# GoodFoods AI Agent - 100 Example Training Dataset

## 📊 Dataset Overview

### Generated Files
- **`training_100.jsonl`**: 100 training examples (72KB)
- **`validation_100.jsonl`**: 1 validation example (552B)
- **Total**: 101 examples following Vertex AI JSONL format

### Dataset Structure
Each line in the JSONL files contains a complete conversation example in the format:
```json
{
  "messages": [
    {"role": "user", "content": "Find restaurants in Koramangala"},
    {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Koramangala'))"},
    {"role": "user", "content": "tool_outputs: [{'id': 1, 'name': 'GoodFoods Koramangala', ...}]"},
    {"role": "model", "content": "I found GoodFoods Koramangala in Koramangala 4th Block, Bangalore..."}
  ]
}
```

## 🎯 Dataset Coverage

### 1. Baseline Conversations (15 examples - 15%)
- Greetings and introductions (Hello, Hi, Good morning/evening)
- FAQ responses (opening hours, locations, capabilities)
- Out-of-scope request handling (weather, jokes)
- Persona establishment (name, role, capabilities)
- General restaurant information (menu, dress code, popular dishes)

### 2. Restaurant Search Scenarios (35 examples - 35%)
- **Location-based searches**: 12 locations (Koramangala, Indiranagar, Jayanagar, Whitefield, Electronic City, MG Road, HSR Layout, Marathahalli, Bellandur, Sarjapur, Hebbal, Yelahanka)
- **Cuisine-based searches**: 12 cuisines (Italian, Chinese, North Indian, South Indian, Continental, Multi-cuisine, Mexican, Thai, Japanese, Mediterranean, American, Fusion)
- **Combined searches**: 5 location-cuisine combinations
- **Multiple restaurant results**: Various scenarios with different numbers of results

### 3. Multi-Turn Booking Dialogues (30 examples - 30%)
- **Information gathering flows**: Complete booking cycles with user details
- **Varied party sizes**: 1-8 people
- **Multiple dates**: today, tomorrow, Friday, Saturday, next week, this weekend, next Monday, next Tuesday
- **Different times**: 7pm, 8pm, 9pm, 7:30pm, 8:30pm, lunch, dinner, 6pm, 10pm
- **Diverse names and phone numbers**: 10 different names, 6 different phone formats
- **Complete booking confirmations**: Full reservation creation with booking IDs

### 4. Menu Specials Queries (10 examples - 10%)
- **General specials requests**: 8 different ways to ask about specials
- **Dietary preference filtering**: vegetarian, vegan, gluten-free, non-vegetarian
- **Price and description formatting**: Proper presentation of menu items

### 5. Error Handling Scenarios (5 examples - 5%)
- **Large party size restrictions**: Parties > 8 people
- **No availability responses**: Empty availability results
- **Invalid booking ID handling**: Non-existent booking cancellations
- **Invalid location searches**: Locations without restaurants

### 6. Context-Aware Confirmations (3 examples - 3%)
- **"Yes" responses after restaurant discovery**: Natural conversation progression
- **Booking flow initiation**: After showing specials
- **Information gathering**: Proper follow-up questions

### 7. Booking Management (2 examples - 2%)
- **Booking detail lookups**: Check existing reservations
- **Cancellation requests**: Cancel confirmed bookings

## 🔧 Tool Integration

The dataset includes examples for all 6 tools with the following distribution:

1. **`check_availability`**: 32 examples (29.4%) - Most common tool
2. **`find_restaurants`**: 31 examples (28.4%) - Second most common
3. **`create_booking`**: 30 examples (27.5%) - Third most common
4. **`get_menu_specials`**: 13 examples (11.9%) - Menu queries
5. **`cancel_booking`**: 2 examples (1.8%) - Cancellation scenarios
6. **`get_booking_details`**: 1 example (0.9%) - Booking lookup

## 📈 Dataset Quality Metrics

### Conversation Flow Patterns
- **Simple queries**: 21% (greetings, FAQs, general info)
- **Tool-calling scenarios**: 79% (all tool interactions)
- **Multi-turn dialogues**: 30% (information gathering)
- **Error handling**: 5% (graceful failure scenarios)

### Conversation Length Statistics
- **Training dataset**: Average 5.4 messages per conversation
- **Validation dataset**: Average 4.0 messages per conversation
- **Range**: 2-10 messages per conversation

### Tool Usage Distribution
- **High-frequency tools**: check_availability, find_restaurants, create_booking (85.3%)
- **Medium-frequency tools**: get_menu_specials (11.9%)
- **Low-frequency tools**: cancel_booking, get_booking_details (2.7%)

## 🎯 Training Objectives

This dataset is designed to train the model to:

1. **Maintain Persona**: Consistent "Samvaad" personality throughout conversations
2. **Handle Context**: Understand "yes" responses in context of previous messages
3. **Select Tools Accurately**: Choose the right tool based on user intent
4. **Gather Information**: Ask for necessary details before proceeding
5. **Handle Errors Gracefully**: Provide helpful responses to edge cases
6. **Format Responses**: Present information clearly and conversationally
7. **Progress Naturally**: Move from discovery to booking seamlessly

## 🚀 Ready for Fine-Tuning

### Dataset Characteristics
- ✅ **Size**: 100 training examples (optimal for cost-effective fine-tuning)
- ✅ **Format**: Vertex AI JSONL format
- ✅ **Coverage**: All tools and conversation types
- ✅ **Quality**: Validated structure and format
- ✅ **Diversity**: Multiple variations and edge cases

### Expected Improvements
After fine-tuning with this dataset, the model should demonstrate:

1. **Better Conversation Flow**: Natural progression from restaurant discovery to booking
2. **Context Awareness**: Understanding "yes" responses in context
3. **Tool Selection**: More accurate tool choice based on user intent
4. **Error Handling**: Graceful responses to edge cases
5. **Persona Consistency**: Maintains "Samvaad" personality throughout
6. **Information Gathering**: Proper follow-up questions for booking details

## 📋 Next Steps

1. **Upload to Google Cloud Storage**:
   ```bash
   gcloud storage cp training_100.jsonl gs://your-bucket-name/datasets/training_100.jsonl
   gcloud storage cp validation_100.jsonl gs://your-bucket-name/datasets/validation_100.jsonl
   ```

2. **Configure Vertex AI Fine-Tuning**:
   - Use `meta/llama3-1-8b` as base model
   - Set appropriate hyperparameters (epochs, learning rate, adapter size)
   - Monitor training progress

3. **Post-Training Testing**:
   - Test conversation flow improvements
   - Verify tool integration
   - Validate error handling
   - Check persona consistency

---

**Generated**: August 2024  
**Dataset Version**: v2.0 (100 examples)  
**Model Target**: Llama 3.1 8B on Vertex AI  
**File Size**: 72KB training, 552B validation 