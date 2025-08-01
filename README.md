# GoodFoods Conversational Reservation Agent

This repository contains the source code for a conversational AI agent designed for the "GoodFoods" restaurant chain. The agent, built with Python and Streamlit, leverages the Llama 3.1 8B language model to provide a seamless, natural language interface for making restaurant reservations.

This project was developed as a submission for the Sarvam AI GenAI Engineer challenge.

## Business Strategy Summary

The current Indian restaurant tech market is dominated by aggregators like Zomato and Swiggy, which own the customer relationship and data. This agent is a strategic initiative for GoodFoods to dis-intermediate these platforms, own its customer data, and provide a premium, branded conversational experience. By automating reservations, the agent aims to significantly improve operational efficiency, reduce staff workload, and decrease revenue loss from no-shows.

### Key Strategic Objectives

- **Dis-intermediation**: Bypass aggregator platforms to build direct customer relationships
- **Operational Efficiency**: Reduce manual reservation handling by 75% within 6 months
- **Revenue Protection**: Decrease no-show rates by 20% through automated reminders
- **Brand Control**: Deliver a consistent, premium conversational experience
- **Data Sovereignty**: Own and leverage first-party customer data for business intelligence

## Architecture

The system follows a modern microservices architecture with containerized deployment:

- **Frontend**: A Streamlit chat interface containerized and deployed separately
- **Backend**: A FastAPI service handling AI logic, database operations, and tool-calling
- **LLM**: Llama 3.1 8B is used as a stateless NLU engine to detect user intent and extract parameters for tool calls
- **Tools**: A set of Python functions that interact with the restaurant database
- **Database**: PostgreSQL with Prisma ORM for production-ready data management

### System Flow

```
User Input → Streamlit Frontend → HTTP API → FastAPI Backend → LLM (Intent Detection) → Tool Execution → Response Generation → Frontend Display
```

### Project Structure

```
GoodFoods-Conversational-Reservation-Agent/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI application
│   │   ├── agent.py            # Core agent logic
│   │   ├── tool_functions.py   # Business logic tools
│   │   ├── tool_definitions.py # Tool schemas
│   │   └── database_schema.py  # Database management
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py                  # Streamlit UI
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml          # For local development
```

## Deployment

### 🚀 Render Deployment (Recommended)

The application is configured for easy deployment to Render with Docker containers.

#### Quick Deployment
1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Render**: 
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" > "Web Service"
   - Connect your GitHub repository
3. **Automatic Deployment**: Render will detect `render.yaml` and deploy both services automatically

#### Manual Deployment
Follow the detailed guide in [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)

#### Environment Variables Required
```bash
# Backend Service
DEV_MODE=false
GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=<your-service-account-json>

# Frontend Service
BACKEND_URL=https://your-backend-service.onrender.com
```

### 🐳 Local Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend: http://localhost:8000
```

### 📋 Deployment Checklist
Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for step-by-step verification.

## Features

### Core Functionality (Green - Implementation Ready)
- **CRUD for Reservations**: Create, Read, Update, and Delete reservations
- **Location/Cuisine-Based Search**: Find restaurants by location or cuisine type
- **Multilingual Support**: English and major Indian languages (Hindi, Kannada, Tamil)
- **Personalized Recommendations**: Suggest restaurants based on user preferences
- **Disambiguation & Context Handling**: Gracefully handle ambiguous queries
- **No-Show Mitigation**: Pre-payment deposits for large groups

### Advanced Features (Yellow - Future Implementation)
- **Real-time Availability Checking**: Live table availability across all locations
- **Smart Recommendations**: AI-powered suggestions based on dining history
- **Automated Reminders**: Proactive booking confirmations and reminders

### Premium Features (Red - Strategic Roadmap)
- **Payment Integration**: Secure deposit collection for large bookings
- **CRM Integration**: Customer relationship management and analytics
- **Proactive Engagement**: Automated feedback collection and loyalty programs

## Setup and Installation

### Prerequisites
- Docker and Docker Compose (for containerized deployment)
- Python 3.8+ (for local development without containers)
- Access to a Llama 3.1 8B API endpoint (e.g., DeepInfra, Ollama, or local deployment)

### Quick Start with Docker (Recommended)

**Option 1: Using startup scripts (easiest)**
```bash
# On macOS/Linux:
./start.sh

# On Windows:
start.bat
```

**Option 2: Manual setup**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharsan99/GoodFoods-Conversational-Reservation-Agent.git
   cd GoodFoods-Conversational-Reservation-Agent
   ```

2. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your API_KEY
   ```

3. **Set up the database:**
   ```bash
   # The database will be automatically initialized with Prisma
   # Make sure your DATABASE_URL is set in .env
   ```

4. **Start the services:**
   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development (Without Docker)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Initialize Prisma and generate client
python init_prisma.py

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Cloud Deployment

For production deployment with PostgreSQL and Prisma, see the comprehensive [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) guide.

For general deployment information, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Prompt Engineering Approach

The agent's intelligence relies on a carefully crafted system prompt that instructs the Llama 3.1 model on its role, capabilities, and response format. The model is explicitly told to use a set of provided tools (defined in a JSON schema) and to respond with a structured JSON object when it decides a tool is necessary. This "from scratch" approach avoids abstraction layers to demonstrate fundamental control over the model's behavior.

### Key Prompting Principles
- **Stateless NLU**: The LLM acts as a stateless intent detection engine
- **Tool-Centric**: All external actions are performed through defined tools
- **Error Resilience**: Robust error handling for malformed LLM outputs
- **Conversational Flow**: State management handled by the application layer

## Example Conversations

### Journey 1: Simple Booking
```
User: Hi, I'd like to book a table for 3 people at GoodFoods Koramangala for this Saturday at 8 PM.
Assistant: Of course! I see a table is available. Just to confirm, that's a booking for 3 people at GoodFoods Koramangala this Saturday at 8:00 PM. Shall I go ahead and confirm it?
User: Yes please.
Assistant: Excellent! Your table is confirmed. Your booking reference is GFS84321. We look forward to seeing you!
```

### Journey 2: Search and Disambiguation
```
User: I want to find a place that serves Italian food.
Assistant: We have a wonderful Italian restaurant at our Indiranagar location. Would you like to know more or book a table there?
User: Book for tomorrow.
Assistant: Certainly. For what time tomorrow were you thinking?
User: Lunch.
Assistant: Perfect. And for how many people?
```

### Journey 3: Multilingual Support
```
User: ನಮಸ್ಕಾರ, ನಾನು ಜಯನಗರದಲ್ಲಿ ಒಂದು ಟೇಬಲ್ ಬುಕ್ ಮಾಡಲು ಬಯಸುತ್ತೇನೆ
Assistant: ನಮಸ್ಕಾರ! ಜಯನಗರದಲ್ಲಿ ನಮ್ಮ GoodFoods ರೆಸ್ಟೋರೆಂಟ್ ಇದೆ. ಎಷ್ಟು ಜನರಿಗೆ ಮತ್ತು ಯಾವ ದಿನಾಂಕಕ್ಕೆ ಬುಕಿಂಗ್ ಬಯಸುತ್ತೀರಿ?
```

## Technical Specifications

### Database Schema
The system uses PostgreSQL with Prisma ORM and includes the following models:
- **Restaurants**: Location details, cuisine types, opening hours
- **Tables**: Physical table inventory and capacities
- **Users**: Customer information and contact details
- **Bookings**: Reservation records with status tracking

The database schema is defined in `backend/prisma/schema.prisma` and automatically managed by Prisma.

### API Endpoints
The backend exposes the following REST API endpoints:
- `POST /chat`: Main chat endpoint for conversation
- `GET /restaurants`: Search restaurants by location or cuisine
- `GET /availability/{restaurant_id}`: Check table availability
- `GET /health`: Health check endpoint
- `GET /docs`: Interactive API documentation

### Tool Definitions
The agent has access to the following tools:
- `find_restaurants(location, cuisine)`: Search for restaurants by location or cuisine
- `check_availability(restaurant_id, date, time, party_size)`: Check real-time table availability
- `create_booking(restaurant_id, user_name, phone_number, date, time, party_size)`: Create new reservations
- `cancel_booking(booking_id)`: Cancel existing bookings

### Performance Parameters
- **Model**: Llama 3.1 8B Instruct
- **Temperature**: 0.1-0.3 (low for deterministic tool calls)
- **Max Tokens**: 512 (optimized for low latency)
- **Response Time**: < 2 seconds for typical queries

## Rollout Strategy

### Phase 1: Internal Pilot (Month 1)
- Deploy on internal website
- Single high-volume location
- Staff training and feedback collection

### Phase 2: Limited Public Launch (Months 2-4)
- 3-5 key urban locations
- Public website integration
- User feedback collection

### Phase 3: Full-Scale Rollout (Months 5-10)
- All GoodFoods locations
- WhatsApp integration
- Marketing campaign launch

### Phase 4: Continuous Enhancement (Ongoing)
- Advanced features implementation
- Proactive engagement capabilities
- Multi-channel expansion

## Assumptions and Limitations

### Current Assumptions
- Stable API access to central Restaurant Management System
- Good faith user interactions
- Reliable Llama 3.1 8B API endpoint availability

### Known Limitations
- **Model Constraints**: Llama 3.1 8B may struggle with complex multi-intent queries
- **No Real Payments**: Pre-payment feature is currently mocked
- **Session Scope**: State management limited to single continuous sessions

## Future Enhancements

### Short-term (3-6 months)
- Migration to Llama 3.1 70B for enhanced conversational capabilities
- Real payment gateway integration
- Advanced error handling and recovery

### Medium-term (6-12 months)
- CRM integration for customer analytics
- Proactive feedback collection
- Voice channel integration (IVR)

### Long-term (12+ months)
- Multi-modal capabilities (image recognition for menu items)
- Predictive analytics for demand forecasting
- Integration with kitchen management systems

## Contributing

This project is developed as a challenge submission. For questions or feedback, please open an issue in the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the Sarvam AI GenAI Engineer challenge
- Leverages Meta's Llama 3.1 8B model
- Powered by Streamlit for the user interface
