# About this project

The objective of this project is to create a Custom ChatGPT with LangChain.


# Create the virtual environment:

```
python -m venv venv
```


## Run the virtual environment:
### Windows
```
venv\Scripts\activate

```
### Linux/MacOS
```
source venv/bin/activate
```

## Install the required Python packages:
```
pip install -r requirements.txt
```


# Set the .env file

1. Copy or rename the `.env_example` to `.env`
2. Get the ChatGPT API key from [their website](https://platform.openai.com/api-keys)
3. Paste it in the `.env` file


# Run Streamlit

```
streamlit run .\chatgpt_with_private_files_and_streamlit.py
```


# Use the Custom ChatGPT with private files

streamlit run .\chatgpt_with_private_files_and_streamlit.py


## Uploading a document
1. Write 1 and press ENTER
2. Write the full path of the document (.pdf, .docx, .txt, or .py) and press ENTER
3. Enter the desired prompt and press ENTER


## Using Wikipedia
1. Write 2 and press ENTER
2. Write the Wikipedia query and press ENTER
3. Enter the desired prompt and press ENTER
