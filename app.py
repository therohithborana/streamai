import streamlit as st
from openai import OpenAI
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Creative Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .output-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'story_history' not in st.session_state:
    st.session_state.story_history = []
if 'image_prompts' not in st.session_state:
    st.session_state.image_prompts = []
if 'client' not in st.session_state:
    st.session_state.client = None

def initialize_openai_api():
    """Initialize OpenAI API with the provided key."""
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        st.session_state.client = OpenAI(api_key=api_key)
        return True
    return False

def generate_content(prompt, content_type="chat", max_tokens=150):
    """Generate content using OpenAI API."""
    try:
        if content_type == "story":
            prompt = f"Write a creative short story about: {prompt}"
            max_tokens = 500
        elif content_type == "image_prompt":
            prompt = f"Generate a detailed, creative image prompt about: {prompt}"
            max_tokens = 100

        response = st.session_state.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def story_generator():
    """Story generation section."""
    st.header("✍️ Story Generator")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        story_theme = st.text_input("Enter a theme or topic for your story:")
        if st.button("Generate Story"):
            if story_theme:
                with st.spinner("Creating your masterpiece... 🎨"):
                    story = generate_content(story_theme, "story")
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.story_history.append((timestamp, story_theme, story))
                    st.markdown(f"### Your Story\n{story}")
    
    with col2:
        if st.session_state.story_history:
            st.subheader("Story History")
            for time, theme, story in st.session_state.story_history[-5:]:
                with st.expander(f"{time} - {theme[:30]}..."):
                    st.write(story)

def image_prompt_generator():
    """Image prompt generation section."""
    st.header("🎨 Image Prompt Generator")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        image_theme = st.text_input("Enter a theme for the image prompt:")
        if st.button("Generate Image Prompt"):
            if image_theme:
                with st.spinner("Crafting the perfect prompt... 🖼️"):
                    prompt = generate_content(image_theme, "image_prompt")
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.image_prompts.append((timestamp, image_theme, prompt))
                    st.markdown(f"### Your Image Prompt\n{prompt}")
    
    with col2:
        if st.session_state.image_prompts:
            st.subheader("Prompt History")
            for time, theme, prompt in st.session_state.image_prompts[-5:]:
                with st.expander(f"{time} - {theme[:30]}..."):
                    st.write(prompt)

def ai_chat():
    """AI chat section."""
    st.header("💭 Chat with AI")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_input("Ask me anything:")
        if st.button("Send Message"):
            if user_input:
                with st.spinner("Thinking... 🤔"):
                    response = generate_content(user_input, "chat")
                    st.session_state.chat_history.append(("You", user_input))
                    st.session_state.chat_history.append(("AI", response))
    
        # Display chat history
        st.subheader("Chat History")
        for role, message in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"**👤 You:** {message}")
            else:
                st.markdown(f"**🤖 AI:** {message}")
    
    with col2:
        st.subheader("Tips")
        st.markdown("""
        - Ask open-ended questions
        - Be specific in your queries
        - Try different topics
        - Have fun exploring!
        """)

def main():
    st.title("🎨 AI Creative Studio")
    
    if not initialize_openai_api():
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        st.markdown("""
        ### How to get an API key:
        1. Go to [OpenAI's website](https://platform.openai.com/api-keys)
        2. Create an account or sign in
        3. Navigate to API section
        4. Create a new API key
        """)
        return

    # Navigation
    page = st.sidebar.radio(
        "Choose a Tool",
        ["Story Generator", "Image Prompt Generator", "AI Chat"]
    )
    
    # Display selected page
    if page == "Story Generator":
        story_generator()
    elif page == "Image Prompt Generator":
        image_prompt_generator()
    else:
        ai_chat()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ using Streamlit and OpenAI")

if __name__ == "__main__":
    main()
