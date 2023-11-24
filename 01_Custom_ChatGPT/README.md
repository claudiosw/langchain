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


# Run the Jupyter Notebook

```
jupyter notebook
```


# Use the Custom ChatGPT

## Use the Custom ChatGPT without memory

1. Open the file `basic_langchain_chatgpt.ipynb` inside of the Jupyter Notebook
2. Press play
3. Enter the desired prompt


## Use the Custom ChatGPT with memory

1. Open the file `langchain_chatgpt_with_memory.ipynb` inside of the Jupyter Notebook
2. Press play
3. Enter the desired prompt. Note that the chatbot will remember the context of previous questions.


## Use the Custom ChatGPT with memory and sessions

1. Open the file `langchain_chatgpt_saving_sessions.ipynb` inside of the Jupyter Notebook
2. Press play
3. Enter the desired prompt. Note that the chatbot will remember the context of previous questions and save the chat history in the `chatbot_history.json` file.
