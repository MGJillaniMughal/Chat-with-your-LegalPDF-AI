import os
import logging
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from htmlTemplates import css, bot_template, user_template
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    @staticmethod
    def read_pdf(pdf_file):
        text = ""
        try:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
        return text

    @staticmethod
    def process_pdf_docs(pdf_docs):
        text = ""
        for pdf in pdf_docs:
            text += PDFProcessor.read_pdf(pdf)
        return text

class ConversationManager:
    @staticmethod
    def get_text_chunks(raw_text):
        # Determine chunk size and overlap based on the length of the text
        total_length = len(raw_text)
        if total_length <= 5000:  # For shorter documents
            chunk_size = 512  # Smaller chunks for smaller documents
            chunk_overlap = 128
        elif 5000 < total_length <= 50000:  # For medium-sized documents
            chunk_size = 1024
            chunk_overlap = 256
        else:  # For very large documents
            chunk_size = 2048  # Larger chunks for larger documents
            chunk_overlap = 512

        # Define the text splitter with dynamic parameters
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["|", "##", ">", "-", "\n", "\\n"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        return text_splitter.split_text(raw_text)


    @staticmethod
    @lru_cache(maxsize=32)  # Caching to avoid reprocessing the same texts
    def get_vector_store(text_chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    @staticmethod
    def get_conversation_chain(vector_store):
        llm = ChatOpenAI(model='gpt-3.5-turbo-1106', temperature=0.2)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory,
        )

class PDFChatbot:
    def __init__(self):
        self.load_env()
        self.setup_streamlit()
        self.initialize_state()

    def load_env(self):
        load_dotenv()

    def setup_streamlit(self):
        st.set_page_config(
            page_title="📚 Chat with your Multiples LAW PDFs",
            page_icon=":books:",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)

    def initialize_state(self):
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None
        if "processed_texts" not in st.session_state:  # Track processed texts
            st.session_state.processed_texts = set()

    def run(self):
        self.display_header()
        self.handle_user_input()
        self.handle_sidebar()

    def display_header(self):
        st.header('📚🔗Chat with your LegalPDF AI')
        st.subheader('Developed by Jillani SoftTech 😎: [JillaniSoftTech](https://www.linkedin.com/in/jillanisofttech/)')

    def handle_user_input(self):
        user_question = st.text_input('Ask a question about your LAW PDFs here: ')
        if user_question:
            self.process_user_input(user_question)

    def handle_sidebar(self):
        with st.sidebar:
            self.display_pdf_uploader()

    def display_pdf_uploader(self):
        st.subheader('Your PDFs')
        pdf_docs = st.file_uploader("⬆️ Upload a PDF or document file and click on 'Process'", 
                                    type=['pdf', "tsv", "csv", "txt", "tab", "xlsx", "xls"], 
                                    accept_multiple_files=True)
        
        if st.button('Process'):
            self.process_uploaded_pdfs(pdf_docs)

    def process_uploaded_pdfs(self, pdf_docs):
        if not pdf_docs:
            st.warning("Please upload a PDF document.")
            return

        with st.spinner('Processing your PDFs...'):
            raw_text = PDFProcessor.process_pdf_docs(pdf_docs)
            if not raw_text.strip():
                st.warning("No text extracted from the uploaded PDFs. Please try a different PDF.")
                return

            # Check if text is already processed
            if raw_text in st.session_state.processed_texts:
                st.info("PDFs already processed.")
                return

            text_chunks = ConversationManager.get_text_chunks(raw_text)
            vector_store = ConversationManager.get_vector_store(tuple(text_chunks))  # Cache key needs to be hashable
            st.session_state.conversation = ConversationManager.get_conversation_chain(vector_store)
            st.session_state.processed_texts.add(raw_text)  # Add to processed texts
            st.success("PDFs processed successfully.")

    def process_user_input(self, user_input):
        try:
            response = st.session_state.conversation({'question': user_input})
            st.session_state.chat_history = response['chat_history']
            self.display_chat_history()
        except Exception as e:
            st.error(f"Error processing user input: {e}")
            logger.error("Error processing user input", exc_info=e)

    def display_chat_history(self):
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace('{{MSG}}', message.content), unsafe_allow_html=True)

if __name__=='__main__':
    chatbot = PDFChatbot()
    chatbot.run()
