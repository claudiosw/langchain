from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_base import llm


def get_summary_prompt_template(text, language):
    template = '''
    Write a concise and short summary of the following text:
    TEXT: `{text}`
    Translate the summary to {language}.
    '''
    prompt = PromptTemplate(
        input_variables=['text', 'language'],
        template=template
    )
    number_of_tokens = llm.get_num_tokens(prompt.format(text=text, language=language))

    if number_of_tokens <= 4000:
        chain = LLMChain(llm=llm, prompt=prompt)
        summary = chain.run({'text': text, 'language':language})
        return summary
    else:
        return 'The text is too long to be summarized by the Basic Prompt method.'
