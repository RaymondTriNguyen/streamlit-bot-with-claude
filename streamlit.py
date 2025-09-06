import streamlit as st
import requests
import json
from typing import Dict, List
import time

# Page configuration
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personality definitions
PERSONALITIES = {
    "Math Teacher": {
        "description": "A knowledgeable mathematics teacher who helps with math problems and concepts",
        "system_prompt": """You are a helpful Math Teacher. You ONLY answer questions related to mathematics, including:
- Arithmetic, algebra, geometry, calculus, statistics
- Math problem solving and explanations
- Mathematical concepts and theories
- Math homework help

If asked about anything outside of mathematics, politely decline and redirect the conversation back to math topics. Always be encouraging and educational in your responses.""",
        "icon": "🧮"
    },
    "Doctor": {
        "description": "A medical professional providing health information and guidance",
        "system_prompt": """You are a helpful Medical Doctor. You ONLY answer questions related to health and medicine, including:
- Symptoms and general health information
- Medical conditions (general information only)
- Wellness and prevention tips
- When to seek medical care

IMPORTANT: Always remind users that your advice is for informational purposes only and they should consult with qualified healthcare providers for medical decisions. If asked about anything outside of health and medicine, politely decline and redirect to medical topics.""",
        "icon": "🩺"
    },
    "Travel Guide": {
        "description": "An experienced travel expert with tips and destination advice",
        "system_prompt": """You are an expert Travel Guide. You ONLY answer questions related to travel, including:
- Destination recommendations and information
- Travel planning and itineraries
- Transportation options
- Accommodation advice
- Local customs and cultures
- Travel tips and safety

If asked about anything outside of travel, politely decline and redirect the conversation back to travel-related topics. Be enthusiastic and helpful about travel experiences.""",
        "icon": "✈️"
    },
    "Chef": {
        "description": "A culinary expert specializing in cooking and recipes",
        "system_prompt": """You are a professional Chef. You ONLY answer questions related to cooking and food, including:
- Recipes and cooking instructions
- Cooking techniques and methods
- Ingredient substitutions and tips
- Kitchen equipment advice
- Food safety and storage
- Cuisine types and food culture

If asked about anything outside of cooking and food, politely decline and redirect the conversation back to culinary topics. Be passionate and detailed about food and cooking.""",
        "icon": "👨‍🍳"
    },
    "Tech Support": {
        "description": "A technical support specialist for devices and software troubleshooting",
        "system_prompt": """You are a Tech Support Specialist. You ONLY answer questions related to technology troubleshooting, including:
- Computer and device problems
- Software installation and configuration
- Network connectivity issues
- Hardware troubleshooting
- Operating system help
- Application support

If asked about anything outside of technical support, politely decline and redirect the conversation back to tech-related topics. Be clear, step-by-step, and patient in your technical explanations.""",
        "icon": "💻"
    }
}

# Available Groq models
GROQ_MODELS = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-90b-text-preview",
    "llama-3.2-11b-text-preview",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""
    if "selected_personality" not in st.session_state:
        st.session_state.selected_personality = "Math Teacher"
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "llama-3.1-70b-versatile"

def call_groq_api(messages: List[Dict], api_key: str, model: str) -> str:
    """Make API call to Groq"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return "Sorry, I encountered an error processing your request."
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return "Request timed out. Please try again."
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error processing your request."

def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []
    st.rerun()

def main():
    init_session_state()
    
    # Title and description
    st.title("🤖 AI Personality Chatbot")
    st.markdown("Chat with AI personalities powered by Groq! Each personality has specific expertise and will only answer questions in their domain.")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "🔑 Groq API Key",
            value=st.session_state.groq_api_key,
            type="password",
            help="Enter your Groq API key. Get one at https://console.groq.com/"
        )
        st.session_state.groq_api_key = api_key
        
        if not api_key:
            st.warning("⚠️ Please enter your Groq API key to start chatting!")
            st.markdown("Get your free API key at [Groq Console](https://console.groq.com/)")
        
        st.divider()
        
        # Model selection
        st.subheader("🧠 AI Model")
        selected_model = st.selectbox(
            "Choose AI Model:",
            GROQ_MODELS,
            index=GROQ_MODELS.index(st.session_state.selected_model),
            help="Different models have varying capabilities and response speeds"
        )
        st.session_state.selected_model = selected_model
        
        st.divider()
        
        # Personality selection
        st.subheader("🎭 Chatbot Personality")
        
        # Display personality options with icons and descriptions
        personality_options = list(PERSONALITIES.keys())
        selected_personality = st.selectbox(
            "Choose Personality:",
            personality_options,
            index=personality_options.index(st.session_state.selected_personality)
        )
        
        # Show personality info
        if selected_personality != st.session_state.selected_personality:
            st.session_state.selected_personality = selected_personality
            # Clear messages when personality changes
            st.session_state.messages = []
        
        personality_info = PERSONALITIES[selected_personality]
        st.markdown(f"**{personality_info['icon']} {selected_personality}**")
        st.markdown(f"*{personality_info['description']}*")
        
        st.divider()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
        
        # Chat statistics
        if st.session_state.messages:
            st.subheader("📊 Chat Stats")
            user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
            assistant_messages = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"])
            st.metric("User Messages", user_messages)
            st.metric("AI Responses", assistant_messages)

    # Main chat interface
    if not api_key:
        st.info("👈 Please enter your Groq API key in the sidebar to start chatting!")
        st.markdown("""
        ### How to get your Groq API key:
        1. Visit [Groq Console](https://console.groq.com/)
        2. Sign up or log in to your account
        3. Navigate to the API Keys section
        4. Create a new API key
        5. Copy and paste it in the sidebar
        """)
        return
    
    # Display current configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"🤖 **Model:** {selected_model}")
    with col2:
        st.info(f"🎭 **Personality:** {selected_personality}")
    with col3:
        st.info(f"💬 **Messages:** {len(st.session_state.messages)}")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask {selected_personality} a question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare messages for API call
        personality_prompt = PERSONALITIES[selected_personality]["system_prompt"]
        api_messages = [{"role": "system", "content": personality_prompt}]
        
        # Add conversation history (limit to last 10 exchanges to manage token usage)
        recent_messages = st.session_state.messages[-20:]  # Last 20 messages (10 exchanges)
        api_messages.extend(recent_messages)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner(f"{selected_personality} is thinking..."):
                response = call_groq_api(api_messages, api_key, selected_model)
                st.markdown(response)
        
        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit and Groq AI | 
            <a href='https://github.com' target='_blank'>View Source</a> | 
            <a href='https://console.groq.com/' target='_blank'>Get Groq API Key</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()