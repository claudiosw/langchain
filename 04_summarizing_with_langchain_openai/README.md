# About this project

The objective of this project is to summarize with LangChain and OpenAI.


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
streamlit run main.py
```