# Fine-Tuning Guide for GoodFoods AI Agent

This guide documents the fine-tuning dataset creation and deployment process for the GoodFoods AI Restaurant Reservation Agent using Google Cloud Vertex AI.

## 📊 Dataset Overview

### Generated Files
- **`training.jsonl`**: 20 training examples (87% of dataset)
- **`validation.jsonl`**: 3 validation examples (13% of dataset)
- **Total**: 23 examples following Vertex AI JSONL format

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

### 1. Baseline Conversations (No Tool-Calling)
- Greetings and introductions
- FAQ responses (opening hours, locations)
- Out-of-scope request handling
- Persona establishment

### 2. Restaurant Search Scenarios
- Location-based searches
- Cuisine-based searches
- Multiple restaurant results
- Single restaurant results

### 3. Multi-Turn Booking Dialogues
- Information gathering flows
- Complete booking cycles
- User confirmation handling
- Context-aware responses

### 4. Menu Specials Queries
- General specials requests
- Dietary preference filtering
- Price and description formatting

### 5. Booking Management
- Cancellation requests
- Booking detail lookups
- Error handling for invalid bookings

### 6. Error Handling Scenarios
- Large party size restrictions
- No availability responses
- Invalid booking ID handling
- Graceful failure responses

### 7. Sequential Tool-Calling
- Multi-step reasoning
- Availability + specials combinations
- Planning and execution flows

### 8. Context-Aware Confirmations
- "Yes" responses after restaurant discovery
- Natural conversation progression
- Booking flow initiation

## 🔧 Tool Integration

The dataset includes examples for all 6 tools:

1. **`find_restaurants`**: Location and cuisine-based searches
2. **`check_availability`**: Table availability verification
3. **`create_booking`**: Final reservation creation
4. **`cancel_booking`**: Booking cancellation
5. **`get_booking_details`**: Booking information lookup
6. **`get_menu_specials`**: Menu specials with dietary filtering

## 📈 Dataset Quality Metrics

### Conversation Flow Patterns
- **Simple queries**: 25% (greetings, FAQs)
- **Tool-calling scenarios**: 75% (all tool interactions)
- **Multi-turn dialogues**: 40% (information gathering)
- **Error handling**: 15% (graceful failure scenarios)

### Tool Usage Distribution
- `find_restaurants`: 35%
- `check_availability`: 25%
- `create_booking`: 20%
- `get_menu_specials`: 10%
- `cancel_booking`: 5%
- `get_booking_details`: 5%

## 🚀 Next Steps: Vertex AI Fine-Tuning

### Prerequisites
1. **Google Cloud Project**: Ensure billing is enabled
2. **Vertex AI API**: Enable the Vertex AI API
3. **Cloud Storage**: Create a bucket for dataset storage
4. **IAM Permissions**: Grant necessary roles to service account

### Dataset Upload
```bash
# Upload training data
gcloud storage cp training.jsonl gs://your-bucket-name/datasets/training.jsonl

# Upload validation data
gcloud storage cp validation.jsonl gs://your-bucket-name/datasets/validation.jsonl
```

### Fine-Tuning Configuration
```python
import vertexai
from vertexai.preview import language_models

# Configuration
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
BASE_MODEL_NAME = "meta/llama3-1-8b"
TRAINING_DATA_URI = "gs://your-bucket-name/datasets/training.jsonl"
VALIDATION_DATA_URI = "gs://your-bucket-name/datasets/validation.jsonl"
TUNED_MODEL_DISPLAY_NAME = "llama3-1-8b-goodfoods-agent-v1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Define tuning job
tuning_job = language_models.SupervisedTuningJob(
    display_name=f"tune-{TUNED_MODEL_DISPLAY_NAME}",
    source_model=BASE_MODEL_NAME,
    train_dataset=TRAINING_DATA_URI,
    validation_dataset=VALIDATION_DATA_URI,
    epoch_count=5,
    adapter_size=8,
    learning_rate_multiplier=1.0
)

# Launch tuning job
tuning_job.run()
print(f"Launched tuning job: {tuning_job.resource_name}")
```

### Expected Improvements
After fine-tuning, the model should demonstrate:

1. **Better Conversation Flow**: Natural progression from discovery to booking
2. **Context Awareness**: Understanding "yes" responses in context
3. **Tool Selection**: More accurate tool choice based on user intent
4. **Error Handling**: Graceful responses to edge cases
5. **Persona Consistency**: Maintains "Samvaad" personality throughout

## 📋 Monitoring and Evaluation

### Training Metrics to Monitor
- **Validation Loss**: Should decrease over epochs
- **Training Loss**: Should decrease but not overfit
- **Tool Accuracy**: Correct tool selection rate
- **Response Quality**: Natural, helpful responses

### Post-Training Testing
1. **Conversation Flow**: Test "yes" responses after restaurant discovery
2. **Tool Integration**: Verify all tools work correctly
3. **Error Scenarios**: Test edge cases and error handling
4. **Persona Consistency**: Ensure "Samvaad" personality is maintained

## 🔄 Iteration Process

### Dataset Expansion
To improve the model further:

1. **Add More Examples**: Increase dataset size to 50-100 examples
2. **Edge Cases**: Include more error scenarios and edge cases
3. **Diverse Conversations**: Add variations in user language and style
4. **Complex Scenarios**: Multi-restaurant comparisons, group bookings

### Hyperparameter Tuning
Experiment with:
- **Epoch Count**: 3-10 epochs
- **Adapter Size**: 4, 8, 16, 32
- **Learning Rate**: 0.5x, 1.0x, 2.0x multiplier

## 📚 References

- [Vertex AI Fine-Tuning Guide](https://cloud.google.com/vertex-ai/docs/general/foundation-models)
- [Llama 3.1 Model Documentation](https://ai.meta.com/llama/)
- [OpenAPI Tool Schema Specification](https://spec.openapis.org/oas/v3.0.3)

## 🎉 Success Criteria

The fine-tuning is successful when the model:
- ✅ Naturally progresses from restaurant discovery to booking
- ✅ Handles "yes" responses contextually
- ✅ Maintains consistent "Samvaad" personality
- ✅ Uses tools accurately and appropriately
- ✅ Provides helpful, conversational responses
- ✅ Handles errors gracefully

---

**Generated**: August 2024  
**Dataset Version**: v1.0  
**Model Target**: Llama 3.1 8B on Vertex AI 