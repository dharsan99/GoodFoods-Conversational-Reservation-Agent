#!/usr/bin/env python3
"""
Dataset Validation Script for GoodFoods AI Agent
Validates the JSONL format and structure for Vertex AI fine-tuning
"""

import json
import sys
from typing import List, Dict, Any

def validate_jsonl_format(filename: str) -> List[Dict[str, Any]]:
    """Validate JSONL file format and return parsed examples"""
    examples = []
    errors = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    example = json.loads(line)
                    examples.append(example)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: JSON decode error - {e}")
                    
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        return []
    
    if errors:
        print(f"❌ Found {len(errors)} JSON format errors:")
        for error in errors:
            print(f"   {error}")
        return []
    
    return examples

def validate_conversation_structure(examples: List[Dict]) -> List[str]:
    """Validate conversation structure and return errors"""
    errors = []
    
    for i, example in enumerate(examples, 1):
        if "messages" not in example:
            errors.append(f"Example {i}: Missing 'messages' field")
            continue
            
        messages = example["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            errors.append(f"Example {i}: Messages must be a list with at least 2 items")
            continue
        
        # Check message structure
        for j, message in enumerate(messages):
            if not isinstance(message, dict):
                errors.append(f"Example {i}, Message {j}: Must be a dictionary")
                continue
                
            if "role" not in message or "content" not in message:
                errors.append(f"Example {i}, Message {j}: Missing 'role' or 'content' field")
                continue
                
            role = message["role"]
            if role not in ["user", "model", "system"]:
                errors.append(f"Example {i}, Message {j}: Invalid role '{role}'")
                continue
        
        # Check role alternation
        for j in range(len(messages) - 1):
            if messages[j]["role"] == messages[j + 1]["role"]:
                errors.append(f"Example {i}: Consecutive messages have same role '{messages[j]['role']}'")
    
    return errors

def analyze_tool_usage(examples: List[Dict]) -> Dict[str, Any]:
    """Analyze tool usage patterns in the dataset"""
    stats = {
        "total_examples": len(examples),
        "tool_calling_examples": 0,
        "tool_types": {},
        "conversation_lengths": [],
        "has_tool_outputs": 0
    }
    
    for example in examples:
        messages = example["messages"]
        stats["conversation_lengths"].append(len(messages))
        
        has_tool_call = False
        has_tool_output = False
        
        for message in messages:
            content = message["content"]
            
            # Check for tool calls
            if "print(restaurant_tools." in content:
                has_tool_call = True
                tool_name = content.split("restaurant_tools.")[1].split("(")[0]
                stats["tool_types"][tool_name] = stats["tool_types"].get(tool_name, 0) + 1
            
            # Check for tool outputs
            if "tool_outputs:" in content:
                has_tool_output = True
        
        if has_tool_call:
            stats["tool_calling_examples"] += 1
        if has_tool_output:
            stats["has_tool_outputs"] += 1
    
    return stats

def main():
    """Main validation function"""
    print("🔍 Validating GoodFoods AI Agent Dataset...")
    print("=" * 50)
    
    # Validate training data
    print("\n📊 Training Dataset Validation:")
    training_examples = validate_jsonl_format("training_100.jsonl")
    if not training_examples:
        print("❌ Training dataset validation failed")
        sys.exit(1)
    
    training_errors = validate_conversation_structure(training_examples)
    if training_errors:
        print("❌ Training dataset structure errors:")
        for error in training_errors:
            print(f"   {error}")
        sys.exit(1)
    
    print(f"✅ Training dataset: {len(training_examples)} examples")
    
    # Validate validation data
    print("\n📊 Validation Dataset Validation:")
    validation_examples = validate_jsonl_format("validation_100.jsonl")
    if not validation_examples:
        print("❌ Validation dataset validation failed")
        sys.exit(1)
    
    validation_errors = validate_conversation_structure(validation_examples)
    if validation_errors:
        print("❌ Validation dataset structure errors:")
        for error in validation_errors:
            print(f"   {error}")
        sys.exit(1)
    
    print(f"✅ Validation dataset: {len(validation_examples)} examples")
    
    # Analyze tool usage
    print("\n🔧 Tool Usage Analysis:")
    training_stats = analyze_tool_usage(training_examples)
    validation_stats = analyze_tool_usage(validation_examples)
    
    print(f"📈 Training Dataset Stats:")
    print(f"   Total examples: {training_stats['total_examples']}")
    print(f"   Tool-calling examples: {training_stats['tool_calling_examples']} ({training_stats['tool_calling_examples']/training_stats['total_examples']*100:.1f}%)")
    print(f"   Examples with tool outputs: {training_stats['has_tool_outputs']}")
    print(f"   Average conversation length: {sum(training_stats['conversation_lengths'])/len(training_stats['conversation_lengths']):.1f} messages")
    
    print(f"\n📈 Validation Dataset Stats:")
    print(f"   Total examples: {validation_stats['total_examples']}")
    print(f"   Tool-calling examples: {validation_stats['tool_calling_examples']} ({validation_stats['tool_calling_examples']/validation_stats['total_examples']*100:.1f}%)")
    print(f"   Examples with tool outputs: {validation_stats['has_tool_outputs']}")
    print(f"   Average conversation length: {sum(validation_stats['conversation_lengths'])/len(validation_stats['conversation_lengths']):.1f} messages")
    
    # Tool distribution
    print(f"\n🛠️ Tool Usage Distribution (Training):")
    total_tools = sum(training_stats['tool_types'].values())
    for tool, count in sorted(training_stats['tool_types'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / total_tools * 100
        print(f"   {tool}: {count} ({percentage:.1f}%)")
    
    # Final validation
    print("\n🎯 Final Validation:")
    
    # Check dataset size recommendations
    total_examples = training_stats['total_examples'] + validation_stats['total_examples']
    if total_examples < 20:
        print("⚠️  Warning: Dataset size is small (< 20 examples). Consider adding more examples.")
    elif total_examples > 500:
        print("⚠️  Warning: Dataset size is large (> 500 examples). May be expensive to train.")
    else:
        print("✅ Dataset size is within recommended range (20-500 examples)")
    
    # Check validation split
    validation_ratio = validation_stats['total_examples'] / total_examples
    if validation_ratio < 0.1:
        print("⚠️  Warning: Validation set is small (< 10%). Consider adding more validation examples.")
    elif validation_ratio > 0.3:
        print("⚠️  Warning: Validation set is large (> 30%). Consider reducing validation examples.")
    else:
        print("✅ Validation split is within recommended range (10-30%)")
    
    # Check tool coverage
    expected_tools = ['find_restaurants', 'check_availability', 'create_booking', 'cancel_booking', 'get_booking_details', 'get_menu_specials']
    missing_tools = [tool for tool in expected_tools if tool not in training_stats['tool_types']]
    if missing_tools:
        print(f"⚠️  Warning: Missing tool examples: {', '.join(missing_tools)}")
    else:
        print("✅ All expected tools are covered in the dataset")
    
    print("\n🎉 Dataset validation complete!")
    print("✅ Ready for Vertex AI fine-tuning")

if __name__ == "__main__":
    main() 