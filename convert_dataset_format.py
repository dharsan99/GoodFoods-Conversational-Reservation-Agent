#!/usr/bin/env python3
"""
Convert dataset from messages format to input_text/output_text format
for Vertex AI fine-tuning
"""

import json
import os

def convert_messages_to_text_format(input_file, output_file):
    """Convert messages format to input_text/output_text format"""
    
    converted_examples = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                example = json.loads(line)
                messages = example.get('messages', [])
                
                if len(messages) < 2:
                    print(f"⚠️  Skipping line {line_num}: insufficient messages")
                    continue
                
                # Convert messages to conversation text
                conversation_text = ""
                for i, message in enumerate(messages):
                    role = message.get('role', '')
                    content = message.get('content', '')
                    
                    if role == 'user':
                        conversation_text += f"User: {content}\n"
                    elif role == 'model':
                        conversation_text += f"Assistant: {content}\n"
                    elif role == 'system':
                        conversation_text += f"System: {content}\n"
                
                # Split into input and output
                lines = conversation_text.strip().split('\n')
                
                if len(lines) < 2:
                    print(f"⚠️  Skipping line {line_num}: insufficient conversation")
                    continue
                
                # Find the last assistant response
                input_lines = []
                output_text = ""
                
                for line in lines:
                    if line.startswith('Assistant:'):
                        if not output_text:  # First assistant response
                            output_text = line.replace('Assistant:', '').strip()
                        else:  # Multiple assistant responses, append to input
                            input_lines.append(line)
                    else:
                        input_lines.append(line)
                
                input_text = '\n'.join(input_lines).strip()
                
                if not input_text or not output_text:
                    print(f"⚠️  Skipping line {line_num}: missing input or output")
                    continue
                
                converted_example = {
                    "input_text": input_text,
                    "output_text": output_text
                }
                
                converted_examples.append(converted_example)
                print(f"✅ Converted example {line_num}")
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON error on line {line_num}: {e}")
                continue
    
    # Write converted examples
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in converted_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Conversion complete!")
    print(f"📁 Input file: {input_file}")
    print(f"📁 Output file: {output_file}")
    print(f"📊 Converted {len(converted_examples)} examples")
    
    return converted_examples

def create_vertex_ai_compatible_dataset():
    """Create Vertex AI compatible dataset"""
    
    print("🔄 Converting dataset to Vertex AI format...")
    
    # Convert training data
    training_converted = convert_messages_to_text_format(
        "training_100.jsonl", 
        "training_vertex_ai.jsonl"
    )
    
    # Convert validation data
    validation_converted = convert_messages_to_text_format(
        "validation_100.jsonl", 
        "validation_vertex_ai.jsonl"
    )
    
    # Show sample of converted format
    if training_converted:
        print("\n📋 Sample converted format:")
        sample = training_converted[0]
        print(f"Input text: {sample['input_text'][:100]}...")
        print(f"Output text: {sample['output_text']}")
    
    return training_converted, validation_converted

def validate_vertex_ai_format(filename):
    """Validate the converted format"""
    print(f"\n🔍 Validating {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                example = json.loads(line)
                
                if 'input_text' not in example:
                    print(f"❌ Line {line_num}: Missing input_text")
                    return False
                
                if 'output_text' not in example:
                    print(f"❌ Line {line_num}: Missing output_text")
                    return False
                
                if not example['input_text'].strip():
                    print(f"❌ Line {line_num}: Empty input_text")
                    return False
                
                if not example['output_text'].strip():
                    print(f"❌ Line {line_num}: Empty output_text")
                    return False
                
            except json.JSONDecodeError as e:
                print(f"❌ Line {line_num}: JSON error - {e}")
                return False
    
    print(f"✅ {filename} format is valid")
    return True

def main():
    """Main conversion function"""
    print("🚀 Converting GoodFoods Dataset to Vertex AI Format")
    print("=" * 60)
    
    # Check if source files exist
    if not os.path.exists("training_100.jsonl"):
        print("❌ training_100.jsonl not found")
        return
    
    if not os.path.exists("validation_100.jsonl"):
        print("❌ validation_100.jsonl not found")
        return
    
    # Convert datasets
    training_converted, validation_converted = create_vertex_ai_compatible_dataset()
    
    # Validate converted format
    print("\n🔍 Validating converted format...")
    training_valid = validate_vertex_ai_format("training_vertex_ai.jsonl")
    validation_valid = validate_vertex_ai_format("validation_vertex_ai.jsonl")
    
    if training_valid and validation_valid:
        print("\n✅ All datasets converted and validated successfully!")
        print("\n📋 Next Steps:")
        print("1. Upload converted datasets to GCS:")
        print("   gsutil cp training_vertex_ai.jsonl gs://goodfoods-datasets-speechtotext-466820/datasets/")
        print("   gsutil cp validation_vertex_ai.jsonl gs://goodfoods-datasets-speechtotext-466820/datasets/")
        print("2. Update fine-tuning script to use new dataset paths")
        print("3. Run fine-tuning with converted datasets")
    else:
        print("\n❌ Validation failed. Please check the errors above.")

if __name__ == "__main__":
    main() 