import streamlit as st
import requests
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GoodFoods - AI Reservation Assistant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .agent-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .user-message {
        background-color: #f5f5f5;
        border-left: 4px solid #666;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Backend URL - can be configured via environment variable
    if "backend_url" not in st.session_state:
        st.session_state.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # Check backend connectivity
    if "backend_connected" not in st.session_state:
        st.session_state.backend_connected = False
        try:
            response = requests.get(f"{st.session_state.backend_url}/health", timeout=5)
            if response.status_code == 200:
                st.session_state.backend_connected = True
        except:
            st.session_state.backend_connected = False

def display_header():
    """Display the main header and description."""
    st.markdown('<h1 class="main-header">GoodFoods AI Reservation Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Welcome to Samvaad - Your intelligent dining companion</p>', unsafe_allow_html=True)
    
    # Display current time
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    st.markdown(f"<p style='text-align: center; color: #888; font-size: 0.9rem;'>Current time: {current_time}</p>", unsafe_allow_html=True)

def display_sidebar():
    """Display the sidebar with additional information and controls."""
    with st.sidebar:
        st.header("About GoodFoods")
        st.markdown("""
        **GoodFoods** is a premium restaurant chain across India, offering diverse cuisines and exceptional dining experiences.
        
        Our AI assistant **Samvaad** can help you:
        - Find restaurants by location or cuisine
        - Check table availability
        - Make reservations
        - Cancel bookings
        - Get booking details
        """)
        
        st.divider()
        
        st.header("Quick Actions")
        if st.button("Clear Conversation", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("Sample Queries", type="secondary"):
            st.session_state.show_samples = True
            st.rerun()
        
        st.divider()
        
        st.header("Backend Status")
        if st.session_state.backend_connected:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Disconnected")
            st.info("Make sure the backend server is running on http://localhost:8000")
        
        st.divider()
        
        st.header("API Documentation")
        st.markdown(f"[View API Docs]({st.session_state.backend_url}/docs)")
        
        st.divider()
        
        st.header("About the AI Agent")
        st.markdown("""
        **Samvaad** uses Llama 3.1 8B model with advanced tool calling capabilities to provide intelligent restaurant assistance.
        
        **Features:**
        - Natural language understanding
        - Tool calling for database operations
        - Conversation memory
        - Multi-step booking process
        """)

def display_sample_queries():
    """Display sample queries for users to try."""
    if st.session_state.get("show_samples", False):
        st.subheader("Try these sample queries:")
        
        samples = [
            "Find restaurants in Koramangala",
            "I want to book a table for 4 people tomorrow at 8 PM",
            "Show me Italian restaurants",
            "Check my booking GF000001",
            "Cancel my booking GF000001",
            "What restaurants serve Chinese food?",
            "Book a table for 2 people at GoodFoods Indiranagar for Friday at 7 PM"
        ]
        
        for i, sample in enumerate(samples, 1):
            if st.button(f"{i}. {sample}", key=f"sample_{i}"):
                st.session_state.sample_query = sample
                st.session_state.show_samples = False
                st.rerun()
        
        if st.button("Close Samples"):
            st.session_state.show_samples = False
            st.rerun()

def send_message_to_agent(message: str) -> str:
    """Send a message to the AI agent and get response."""
    try:
        # Prepare the request
        payload = {
            "message": message,
            "conversation_history": st.session_state.messages
        }
        
        # Send request to backend
        response = requests.post(
            f"{st.session_state.backend_url}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["response"]
        else:
            return f"Error: Backend returned status code {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {str(e)}"
    except Exception as e:
        return f"Error processing request: {str(e)}"

def display_chat_interface():
    """Display the main chat interface."""
    st.subheader("Chat with Samvaad")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle sample query if set
    if hasattr(st.session_state, 'sample_query'):
        user_message = st.session_state.sample_query
        del st.session_state.sample_query
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Samvaad is thinking..."):
                response = send_message_to_agent(user_message)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Chat input
    if prompt := st.chat_input("How can I help you book a table?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Samvaad is thinking..."):
                response = send_message_to_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def display_footer():
    """Display the footer with additional information."""
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>GoodFoods AI Reservation Assistant | Powered by Llama 3.1 8B</p>
        <p>Built with FastAPI, Streamlit, and Google Cloud Vertex AI</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Display sample queries if requested
    display_sample_queries()
    
    # Main content area
    if st.session_state.backend_connected:
        # Display chat interface
        display_chat_interface()
    else:
        # Show connection error
        st.error("⚠️ Cannot connect to the backend server")
        st.info("""
        Please make sure the backend server is running:
        
        1. Open a terminal in the `backend` directory
        2. Run: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
        3. Refresh this page once the server is running
        """)
        
        # Show backend status check
        if st.button("Check Backend Connection"):
            try:
                response = requests.get(f"{st.session_state.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    st.session_state.backend_connected = True
                    st.success("✅ Backend is now connected!")
                    st.rerun()
                else:
                    st.error(f"Backend returned status code: {response.status_code}")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")
    
    # Display footer
    display_footer()

if __name__ == "__main__":
    main() 