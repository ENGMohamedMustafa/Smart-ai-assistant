# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath("services"))
from translation_service import TranslationService


import streamlit as st
import os
from pathlib import Path
import tempfile
import asyncio
from datetime import datetime

# Import custom services
from services.whisper_service import WhisperService
from services.translation_service import TranslationService

from services.rag_service import RAGService
from services.dalle_service import DalleService
from services.tts_service import TTSService
from utils.session_manager import SessionManager
from config.settings import Settings

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all AI services"""
    return {
        'whisper': WhisperService(),
        'translator': TranslationService(),
        'rag': RAGService(),
        'dalle': DalleService(),
        'tts': TTSService(),
        'session': SessionManager()
    }

def main():
    st.set_page_config(
        page_title="Multi-Modal AI Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Initialize services
    services = initialize_services()
    
    # Sidebar configuration
    with st.sidebar:
        st.title("🧠 AI Assistant")
        st.markdown("---")
        
        # Language selection
        target_language = st.selectbox(
            "🌍 Target Language",
            ["Arabic", "English", "French", "Spanish", "German"],
            index=0
        )
        
        # Input method selection
        input_method = st.radio(
            "📝 Input Method",
            ["Text", "Audio Upload", "Live Recording"]
        )
        
        # Feature toggles
        st.markdown("### Features")
        enable_translation = st.checkbox("🔄 Translation", value=True)
        enable_rag = st.checkbox("📚 RAG Search", value=True)
        enable_image_gen = st.checkbox("🎨 Image Generation", value=True)
        enable_tts = st.checkbox("🔊 Text-to-Speech", value=True)
        
        # Session management
        st.markdown("---")
        if st.button("🗑️ Clear Session"):
            st.session_state.clear()
            st.rerun()
    
    # Main interface
    st.title("🧠 Multi-Modal AI Assistant")
    st.markdown("### Powered by RAG + Whisper + DALL·E + Translation")
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Knowledge Base", "🎨 Image Gallery", "📊 Analytics"])
    
    with tab1:
        handle_chat_interface(services, input_method, target_language, 
                            enable_translation, enable_rag, enable_image_gen, enable_tts)
    
    with tab2:
        handle_knowledge_base(services['rag'])
    
    with tab3:
        handle_image_gallery(services['dalle'])
    
    with tab4:
        handle_analytics(services['session'])

def handle_chat_interface(services, input_method, target_language, 
                         enable_translation, enable_rag, enable_image_gen, enable_tts):
    """Main chat interface handler"""
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display additional content (images, audio)
            if "image" in message:
                st.image(message["image"], caption="Generated Image")
            if "audio" in message:
                st.audio(message["audio"])
    
    # Input handling based on method
    user_input = None
    
    if input_method == "Text":
        user_input = st.chat_input("Type your message...")
    
    elif input_method == "Audio Upload":
        uploaded_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'm4a'])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(uploaded_file.read())
                user_input = services['whisper'].transcribe(tmp_file.name)
                os.unlink(tmp_file.name)
                
                if user_input:
                    st.success(f"Transcribed: {user_input}")
    
    elif input_method == "Live Recording":
        if st.button("🎤 Start Recording"):
            # Note: Live recording would require additional setup with browser APIs
            st.info("Live recording feature would require WebRTC integration")
    
    # Process user input
    if user_input:
        process_user_input(services, user_input, target_language, 
                          enable_translation, enable_rag, enable_image_gen, enable_tts)

def process_user_input(services, user_input, target_language, 
                      enable_translation, enable_rag, enable_image_gen, enable_tts):
    """Process user input through various AI services"""
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Process with AI assistant
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_data = {}
        
        # Step 1: Translation (if enabled)
        if enable_translation and target_language != "English":
            translated_input = services['translator'].translate(user_input, target_language)
            response_data['translation'] = translated_input
            response_placeholder.markdown(f"**Translation:** {translated_input}")
        
        # Step 2: RAG-enhanced response (if enabled)
        if enable_rag:
            rag_response = services['rag'].get_response(user_input)
            response_data['rag_response'] = rag_response
            response_placeholder.markdown(f"**RAG Response:** {rag_response}")
        
        # Step 3: Image generation (if requested and enabled)
        if enable_image_gen and any(keyword in user_input.lower() for keyword in 
                                   ['generate image', 'create picture', 'draw', 'صورة', 'رسم']):
            with st.spinner("Generating image..."):
                image_url = services['dalle'].generate_image(user_input)
                if image_url:
                    response_data['image'] = image_url
                    st.image(image_url, caption="Generated Image")
        
        # Step 4: Text-to-speech (if enabled)
        if enable_tts:
            final_response = response_data.get('rag_response', user_input)
            audio_file = services['tts'].generate_speech(final_response, target_language)
            if audio_file:
                response_data['audio'] = audio_file
                st.audio(audio_file)
        
        # Save complete response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_data.get('rag_response', 'Response generated'),
            **{k: v for k, v in response_data.items() if k != 'rag_response'}
        })

def handle_knowledge_base(rag_service):
    """Knowledge base management interface"""
    st.subheader("📚 Knowledge Base Management")
    
    # Upload documents
    uploaded_files = st.file_uploader(
        "Upload Documents", 
        type=['pdf', 'txt', 'docx'], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if st.button(f"Process {file.name}"):
                with st.spinner(f"Processing {file.name}..."):
                    success = rag_service.add_document(file)
                    if success:
                        st.success(f"✅ {file.name} added to knowledge base")
                    else:
                        st.error(f"❌ Failed to process {file.name}")
    
    # Display current knowledge base stats
    stats = rag_service.get_stats()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Documents", stats.get('document_count', 0))
    with col2:
        st.metric("Chunks", stats.get('chunk_count', 0))
    with col3:
        st.metric("Vector Dimensions", stats.get('vector_dims', 0))

def handle_image_gallery(dalle_service):
    """Image gallery interface"""
    st.subheader("🎨 Generated Images Gallery")
    
    # Display generated images
    images = dalle_service.get_generated_images()
    
    if images:
        cols = st.columns(3)
        for idx, img_data in enumerate(images):
            with cols[idx % 3]:
                st.image(img_data['url'], caption=img_data['prompt'])
                st.caption(f"Generated: {img_data['timestamp']}")
    else:
        st.info("No images generated yet. Start chatting to create some!")

def handle_analytics(session_manager):
    """Analytics dashboard"""
    st.subheader("📊 Usage Analytics")
    
    analytics = session_manager.get_analytics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Messages", analytics.get('total_messages', 0))
        st.metric("Images Generated", analytics.get('images_generated', 0))
    
    with col2:
        st.metric("Documents Processed", analytics.get('documents_processed', 0))
        st.metric("Audio Files Processed", analytics.get('audio_processed', 0))

if __name__ == "__main__":
    main()