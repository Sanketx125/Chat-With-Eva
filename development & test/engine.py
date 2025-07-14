import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDqeB4cF5WEaS56TM0oRtA2Qd3XKRVEv6A"

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.vectorstores import Chroma
import storage as s
from dotenv import load_dotenv

load_dotenv()
parser = StrOutputParser()

# models
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
embbeding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    temperature=0,
)

# pdf loader
#loader = PyPDFLoader("D:\\BTech\\3-YEAR\\#6- SEM\\web application development\\Web Technology.pdf")
loader = PyPDFLoader(s.pdf_file)
pages = loader.load_and_split()


# vecter store
vector_store = Chroma(
    embedding_function= embbeding_model,
    collection_name= 'sample',
    persist_directory= './db'
)

# testing 
#s.user_message = input("Ask: ")

# MMR Retriver
retrieved_docs = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5,  "lambda_mult": 0.5}
)

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

parallel_chain = RunnableParallel({
    'context': retrieved_docs | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})

# Augmentation text
prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)

main_chain = parallel_chain | prompt | model | parser




s.ai_response = main_chain.invoke(s.user_message)

#test
#print(f'AI : {s.ai_response}')







