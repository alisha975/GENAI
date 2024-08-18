#RAG-POWERED PDF Q&A APP


This project is a Retrieval-Augumented Generation(RAG) built uisng AZURE OpenAI and Streamlit. This app allows users to upload a theory PDF(up to 200 MB) and asked question related to the content of that PDF.
This app will then provide responses based on the content of the uploaded document.

FEATURES

1. Upload PDF files: Users can upload PDFs(up to 200 MB) contaning theory or other content.
2. Interactive Q&A: Ask questions about the content of the uploaded PDF and get accurate responses generated uisng GPT LLm model.
3. Streamlit UI : A user-friendly interface powered by Streamlit, making the app easy to use.


INSTALLATION

1.clone the Repository: 

          git clone https://github.com/alisha975/GENAI.git
          
          cd RAG_WITH_AZURE
          
2.Set UP a Virtual Environment:

           python -m venv env
           
           venv\Scripts\activate

3.Instqall dependencies: 

          pip install -r requirements.txt

4.Set Up Azure OPENAI environment just change your own credential and paste in code azure.py

          os.environ["AZURE_OPENAI_API_KEY"] = "XXX YOUR AZURE API KEY XXXX"
          os.environ["AZURE_OPENAI_ENDPOINT"] = "XXX YOUR AZURE ENDPOINT XXX"
          os.environ["AZURE_OPENAI_API_VERSION"] = "XXX YOUR AZURE API VERSION XXX"
          os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "XXX YOUR AZURE DEPLOYMENT NAME"

5.Run the APP: 

          Streamlit run azure.py

