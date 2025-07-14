import os
os.environ["GOOGLE_API_KEY"] = "API Key"

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()



embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    temperature=0,
)

chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

def create_vector_store(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    texts = [doc.page_content for doc in pages]

    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embedding_model,
        persist_directory='./db',
        collection_name='sample'
    )

    vector_store.persist()
    return vector_store

def answer_question(question):
    vector_store = Chroma(
        embedding_function=embedding_model,
        persist_directory='./db',
        collection_name='sample'
    )
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "lambda_mult": 0.5}
    )

    docs = retriever.get_relevant_documents(question)
    context_text = "\n\n".join(doc.page_content for doc in docs)

    

    prompt_template = PromptTemplate(
        template="""
            You are a friendly and intelligent assistant named **Eva**. 
            Speak naturally and kindly like a close friend. Avoid repeating phrases like "Hello" or "Based on the transcript..." — keep your answers direct and helpful.

            Here’s how you behave:
            - When the user asks something related to the provided context, give a clear, confident, and helpful answer **only using that context**.
            - If the user asks general or casual questions (like "How are you?" or "What’s your name?"), respond sweetly and warmly like a friend, but kindly remind them that you can only answer questions based on the transcript.
            - If the context doesn’t contain an answer, respond politely with something like:  
            “Hmm… I couldn’t find anything about that in the transcript. Want to ask something else?”

            Never make up answers or guess anything that’s not in the transcript.

            ---

            Transcript context:
            {context}

            User's question:
            {question}

            Your answer:
        """,
        input_variables=["context", "question"]
    )


    prompt = prompt_template.format(context=context_text, question=question)
    response = chat_model.invoke(prompt)
    return response.content
