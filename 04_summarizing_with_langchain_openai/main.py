import streamlit as st
import os
import tiktoken
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=False) 


from langchain_base import load_document, chunk_data
from summarize \
    import get_summary_using_basic_prompt, get_summary_using_map_reduce,\
    get_summary_using_map_reduce,get_summary_using_map_reduce_with_template,\
    get_summary_prompt_template,get_stuff_summarize_chain, get_summary_using_refine, \
    get_summary_using_refine_with_template


def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']
    if 'question_input' in st.session_state:
        del st.session_state.question_input


def calculate_embedding_cost(texts):
    enc = tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
    return total_tokens, total_tokens / 1000 * 0.0004


if __name__ == "__main__":
    #data = None
    file_name = ""

    st.subheader('LLM Question-Answering Application ')
    with st.sidebar:
        # text_input for the OpenAI API key (alternative to python-dotenv and .env)
        api_key = st.text_input('OpenAI API Key:', type='password')
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key

        uploaded_file = st.file_uploader('Upload a file:', type=['pdf', 'docx', 'txt', 'py'])
        chunk_size = st.number_input('Chunk size:', min_value=100, max_value=4096, value=4000, on_change=clear_history)
        k = st.number_input('k', min_value=1, max_value=20, value=3, on_change=clear_history)
        add_data = st.button('Add Data', on_click=clear_history)
        if uploaded_file and add_data:
            with st.spinner('Reading, chunking and embedding file...'):
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name)
                print(f"file_name={file_name}")
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)
                data = load_document(file_name)
                #print(f"data0={data}")
                chunks = chunk_data(data, chunk_size=chunk_size)
                st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')
                tokens, embedding_cost = calculate_embedding_cost(chunks)
                st.write(f'Embedding cost: ${embedding_cost:.4f}')
                chunks = chunk_data(data)
                st.success('File chunked successfully.')
                st.session_state.data = data

    option_method = st.selectbox(
        'Choose summarization method',
        ('', 'Basic', 'Basic with template', 'Map Reduce', 'Map Reduce with template', 'Refine', 'Stuffing')
    )
    if option_method:
        with st.spinner('Getting the answer...'):
            print(f"file_name={file_name}")
            data = st.session_state.data
            print(f"data={data}")
            if option_method == 'Basic':
                result = get_summary_using_basic_prompt(str(data))
            elif option_method == 'Basic with template':
                result = get_summary_prompt_template(str(data), "English")
            elif option_method == 'Map Reduce':
                result = get_summary_using_map_reduce(str(data))
            elif option_method == 'Map Reduce with template':
                result = get_summary_using_map_reduce_with_template(str(data))
            elif option_method == 'Refine':
                result = get_summary_using_refine(data)
            elif option_method == 'Stuffing':
                result = get_stuff_summarize_chain(str(data))
            else:
                result = ""
            if result != "":
                st.write(f'LLM Answer: \n {result}')
                print('Ok')
