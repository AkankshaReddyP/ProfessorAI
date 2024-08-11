import os
import streamlit as st
import time
import requests
from bs4 import BeautifulSoup
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document  # Import the correct Document schema

# Set the OpenAI API key directly from the first line
api_key = ""
os.environ['OPENAI_API_KEY'] = api_key

st.title("ProfessorAI: Research About your Professor")
st.sidebar.title("Select a Professor")

# Create a dictionary of professor names and their corresponding IDs
professors = {
    "Amin Alipour": 2452945,
    "Guoning Chen": 2185985,
    "Albert Cheng": 230431,
    "Rathish Das": 3023528,
    "Zhigang Deng": 1291648,
    "Christoph Eick": 132230,
    "Omprakash Gnawali": 1680525,
    "Stephen S.-H. Huang": 2684190,
    "Lennart Johnsson": 230439,
    "Ioannis Kakadiaris": 230440,
    "Ernst Leiss": 230441,
    "Sen Lin": 2956565,
    "Jinyang Liu": 523460,
    "Arjun Mukherjee": 2173365,
    "Carlos Ordonez": 1473876,
    "Gopal Pandurangan": 2349455,
    "Ioannis Pavlidis": 1736447,
    "Shishir Shah": 1262082,
    "Weidong (Larry) Shi": 1517584,
    "Thamar Solorio": 2068023,
    "Jaspal Subhlok": 132213,
    "Nikolaos V. Tsekos": 1685589,
    "Rakesh Verma": 191067,
    "Panruo Wu": 2472665,
    "Feng Yan": 2957965
}

# Create a dropdown for professors
professor_name = st.sidebar.selectbox("Choose a professor", list(professors.keys()))
professor_id = professors[professor_name]
process_professor_clicked = st.sidebar.button("Process Professor")

file_path = "faiss_store_openai.pkl"
main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

# Initialize embeddings outside the button click handler
embeddings = OpenAIEmbeddings()

if process_professor_clicked:
    try:
        # Use the professor ID to construct the URL or fetch data directly
        url = f"https://www.ratemyprofessors.com/professor/{professor_id}"

        # Fetch the content using requests
        main_placeholder.text("Data Loading...Started...✅✅✅")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.get_text(separator='\n')  # Extract text with newline separator

        if not data.strip():
            st.error("No data loaded. Please check the URL content and try again.")
        else:
            # Create a Document object with source metadata
            document = Document(page_content=data, metadata={"source": url})

            # Split data
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            main_placeholder.text("Text Splitter...Started...✅✅✅")
            docs = text_splitter.split_documents([document])

            # Create embeddings and save them to FAISS index
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
            main_placeholder.text("Embedding Vector Started Building...✅✅✅")
            time.sleep(2)

            # Save the FAISS index to a local file
            vectorstore_openai.save_local(file_path)

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching data: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        # Load the FAISS index directly from the saved file
        vectorstore = FAISS.load_local(file_path, embeddings, allow_dangerous_deserialization=True)
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
        result = chain({"question": query}, return_only_outputs=True)
        # result will be a dictionary of this format --> {"answer": "", "sources": [] }
        st.header("Answer")
        st.write(result["answer"])

        # Display sources, if available
        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write(source)
