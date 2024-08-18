import streamlit as st
from langchain.chat_models import AzureChatOpenAI
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


##Azure credential
os.environ["AZURE_OPENAI_API_KEY"] = "XXX YOUR AZURE API KEY XXXX"
os.environ["AZURE_OPENAI_ENDPOINT"] = "XXX YOUR AZURE ENDPOINT XXX"
os.environ["AZURE_OPENAI_API_VERSION"] = "XXX YOUR AZURE API VERSION XXX"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "XXX YOUR AZURE DEPLOYMENT NAME"


template = """Use the following pieces of context to answer the question at the end. Keep the answer accurate and answer should be in brief. if answer is in step include all the steps and step should be accurate. Always say "thanks for asking!" at the end of the answer. 
    {context}
    Question: {question}
    Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

@st.cache_data
def load_parse_document(path_file):
    loader = PyMuPDFLoader(path_file)
    data = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=800,chunk_overlap=10)
    texts = text_splitter.split_documents(data)
    return texts


##Generte Response
def retrive_response(texts,question):

    ##create Embedding
    embedding = AzureOpenAIEmbeddings(model="text-embedding-3-large")

    ##create doc_search db
    doc_search = Chroma.from_documents(texts,embedding, persist_directory='chroma')

    ##create model
    model = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    temperature=0.0
    )

    ##create chain function
    chain = RetrievalQA.from_chain_type(
        model,
        return_source_documents=True,
        retriever=doc_search.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    answer=chain.invoke({"query": question})
    return answer['result']


st.title("Welcome to UQA")
st.write("UQA means UPLOAD QUESTION and ANSWER Here you have to upload your pdf file less thn 200 MB. After uploading your\
          file you have to wait for confirmation message for uploading then you can ask any question related to your pdf file.\
          your question asking tab shows after you succed in uploading pdf file")

uploaded_file=st.file_uploader("choose a pdf file",type="pdf")
if uploaded_file is not None:
    with open("temp_uploaded_file.pdf","wb") as f:
        f.write(uploaded_file.getbuffer())
    path_file="temp_uploaded_file.pdf"
    texts=load_parse_document(path_file)
    st.write(f"your pdf file is uploaded.")
    st.write("Now you can ask question related to your pdf")
    prompt=st.text_input("Write your question")
    if prompt is not None:
        st.write(f"you asked {prompt}")
        question= prompt
        response=retrive_response(texts,question)
        st.write(f"Response: {response}")







