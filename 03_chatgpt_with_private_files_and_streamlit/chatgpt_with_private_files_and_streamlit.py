import streamlit as st
import os
import tiktoken
from langchain.document_loaders \
    import PyPDFLoader, Docx2txtLoader, TextLoader, WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
from langchain.vectorstores import Pinecone as PineconeLangChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv


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


def chunk_data(data, chunk_size=256, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(data)



def insert_or_fetch_embeddings(index_name, chunks):
    embeddings = OpenAIEmbeddings()
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    PINECONE_API_ENV = os.environ.get("PINECONE_ENV")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    if index_name in pinecone.list_indexes():
        print(f'Index {index_name} already exists. Loading embeddings... ', end='')
        vector_store = PineconeLangChain.from_existing_index(index_name, embeddings)
        print('Ok')
    else:
        print(f'Creating index {index_name} and embeddings...', end='')
        pinecone.create_index(index_name, dimension=1536, metric='cosine')
        vector_store = PineconeLangChain.from_documents(chunks, embeddings, index_name=index_name)
        print('Ok')
    return vector_store

def delete_pinecone_index(index_name='all'):
    PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
    PINECONE_API_ENV = os.environ.get("PINECONE_ENV")
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    if index_name == 'all':
        indexes = pinecone.list_indexes()
        print('Deleting all indexes... ')
        for index in indexes:
            pinecone.delete_index(index)
        print('Ok')
    else:
        print(f'Deleting index {index_name}...', end='')
        pinecone.delete_index(index_name)
        print('Ok')

def ask_and_get_answer(vector_store, q, k=3):
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(q)
    return answer


def calculate_embedding_cost(texts):
    enc = tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    return total_tokens, total_tokens / 1000 * 0.0004


def clear_question_input():
    st.session_state.question = st.session_state.question_input
    del st.session_state.question_input


def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']
    if 'question_input' in st.session_state:
        del st.session_state.question_input


if __name__ == "__main__":

    st.subheader('LLM Question-Answering Application 🤖')
    with st.sidebar:
        # text_input for the OpenAI API key (alternative to python-dotenv and .env)
        api_key = st.text_input('OpenAI API Key:', type='password')
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key

        uploaded_file = st.file_uploader('Upload a file:', type=['pdf', 'docx', 'txt', 'py'])
        chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)
        k = st.number_input('k', min_value=1, max_value=20, value=3, on_change=clear_history)
        add_data = st.button('Add Data', on_click=clear_history)
        if uploaded_file and add_data:
            with st.spinner('Reading, chunking and embedding file...'):
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)
                data = load_document(file_name)
                chunks = chunk_data(data, chunk_size=chunk_size)
                st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')
                tokens, embedding_cost = calculate_embedding_cost(chunks)
                st.write(f'Embedding cost: ${embedding_cost:.4f}')
                delete_pinecone_index()
                chunks = chunk_data(data)
                index_name = 'chatgpt'
                vector_store = vector_store = insert_or_fetch_embeddings(index_name, chunks)

                # saving the vector store in the streamlit session state (to be persistent between reruns)
                st.session_state.vs = vector_store
                st.success('File uploaded, chunked and embedded successfully.')

    st.text_input('Ask a question about the content of your file:', key="question_input", on_change=clear_question_input)
    if 'question' in st.session_state:
        q = st.session_state.question
    else:
        q = ""
    if q:
        STANDARD_ANSWER = "Answer only based on the text you received as input. Don't search external sources. " \
                          "If you can't answer then return `I DONT KNOW`."
        q = f"{q} {STANDARD_ANSWER}"
        if 'vs' in st.session_state: # if there's the vector store (user uploaded, split and embedded a file)
            with st.spinner('Getting the answer...'):
                print('Getting the answer...')
                vector_store = st.session_state.vs
                answer = ask_and_get_answer(vector_store, q, k)
                st.write(f'LLM Answer: \n {answer}')
                st.divider()
                value = f'Q: {q} \nA: {answer}'
                to_add_in_history = f'{value} \n {"-" * 100}'

                if 'history' not in st.session_state:
                    st.session_state.history = to_add_in_history
                else:
                    st.session_state.history = f'{to_add_in_history} \n {st.session_state.history}'
                h = st.session_state.history
                st.text_area(label='Chat History', key='history', height=400)
                print('Ok')
