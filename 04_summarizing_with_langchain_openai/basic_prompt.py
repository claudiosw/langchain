from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage


def get_summary_using_basic_prompt(text):
    messages = [
        SystemMessage(content='You are an expert copywriter with expertize in summarizing documents'),
        HumanMessage(content=f'Please provide a short and concise summary of the following text:\n TEXT: {text}')
    ]
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    if llm.get_num_tokens(text) <= 4000:
        summary_output = llm(messages)
        return summary_output.content
    else:
        return 'The text is too long to be summarized by the Basic Prompt method.'
