import os
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders \
    import PyPDFLoader, Docx2txtLoader, TextLoader, WikipediaLoader
from dotenv import load_dotenv, find_dotenv


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')


def get_chunks_from_text(text, chunk_size=10000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.create_documents([text])
    return chunks


def chunk_data(data, chunk_size=10000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    return chunks


load_dotenv(find_dotenv(), override=False) 

def load_document(file):
    name, extension = os.path.splitext(file)
    if extension == '.pdf':
        print(f'Loading {file}')
        document_loader = PyPDFLoader(file)
    elif extension == '.docx':
        print(f'Loading {file}')
        document_loader = Docx2txtLoader(file)
    elif extension in ('.txt', '.py'):
        document_loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None
    return document_loader.load()
