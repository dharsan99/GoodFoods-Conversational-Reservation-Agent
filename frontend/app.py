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
        
        if st.button("Check Backend Status", type="secondary"):
            try:
                response = requests.get(f"{st.session_state.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    st.success("Backend is connected and healthy!")
                else:
                    st.error("Backend is not responding properly")
            except Exception as e:
                st.error(f"Backend connection failed: {str(e)}")
            st.rerun()
        
        st.divider()
        
        st.header("Contact Information")
        st.markdown("""
        **Customer Support:** +91-1800-GOODFOODS  
        **Email:** support@goodfoods.in  
        **Hours:** 24/7 AI Support
        """)
        
        st.divider()
        
        # Display conversation stats
        if st.session_state.messages:
            st.header("Conversation Stats")
            st.metric("Messages", len(st.session_state.messages))
            st.metric("Backend Status", "Connected" if st.session_state.backend_connected else "Disconnected")

def display_sample_queries():
    """Display sample queries for users to try."""
    if st.session_state.get("show_samples", False):
        st.markdown("### Try these sample queries:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Find Restaurants:**")
            sample_queries = [
                "Find restaurants in Koramangala",
                "Show me Italian restaurants",
                "I want to find GoodFoods near Indiranagar",
                "What restaurants serve North Indian food?"
            ]
            
            for query in sample_queries:
                if st.button(query, key=f"sample_{query[:20]}"):
                    st.session_state.user_input = query
                    st.session_state.show_samples = False
                    st.rerun()
        
        with col2:
            st.markdown("**Make Bookings:**")
            booking_queries = [
                "Book a table for 4 people tomorrow at 8 PM",
                "I need a reservation for 2 at GoodFoods Koramangala",
                "Check availability for 6 people this Saturday",
                "Cancel my booking GFS00001"
            ]
            
            for query in booking_queries:
                if st.button(query, key=f"sample_{query[:20]}"):
                    st.session_state.user_input = query
                    st.session_state.show_samples = False
                    st.rerun()

def display_chat_interface():
    """Display the main chat interface."""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How can I help you book a table today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            if st.session_state.backend_connected:
                with st.spinner("Thinking..."):
                    try:
                        # Call the backend API
                        api_response = requests.post(
                            f"{st.session_state.backend_url}/chat",
                            json={
                                "message": prompt,
                                "history": st.session_state.messages
                            },
                            timeout=30
                        )
                        
                        if api_response.status_code == 200:
                            response_data = api_response.json()
                            response = response_data["reply"]
                            st.markdown(response)
                        else:
                            st.error(f"Backend error: {api_response.status_code}")
                            response = "I apologize, but I encountered an error. Please try again."
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {str(e)}")
                        response = "I apologize, but I cannot connect to the backend service. Please check your configuration."
            else:
                st.error("Backend not connected. Please check the backend service.")
                response = "I apologize, but I'm currently unavailable. Please check the backend connection."
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_footer():
    """Display the footer with additional information."""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Supported Languages**")
        st.markdown("English, Hindi, Kannada, Tamil")
    
    with col2:
        st.markdown("**Available Cities**")
        st.markdown("Bangalore, Mumbai, Delhi, Chennai, Hyderabad, Pune, Kolkata, Ahmedabad")
    
    with col3:
        st.markdown("**Cuisines**")
        st.markdown("North Indian, South Indian, Chinese, Italian, Continental, and more")

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
    
    # Display main chat interface
    display_chat_interface()
    
    # Display footer
    display_footer()
    
    # Handle user input from sample queries
    if hasattr(st.session_state, 'user_input'):
        del st.session_state.user_input

if __name__ == "__main__":
    main() 