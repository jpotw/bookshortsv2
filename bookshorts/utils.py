from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo")


def summarize(title, author):
    template = """
    Don't say, just do:  
    '''
    당신은 세계 최고의 책 요약 전문가입니다.
    {author}가 쓴 {title}의 내용을 누구보다 잘 요약해주세요.
    책의 가장 핵심적인 인사이트를 설명해주세요.
    '''
    """
    prompt = PromptTemplate(template=template, input_variables=["text"])
    template.format(author=author, title=title)
    chain = load_summarize_chain(llm=llm, 
                             chain_type='Stuff', 
                             verbose=True)
    return chain.run()