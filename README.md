# ProfessorAI: Research About Your Professor


#### Introduction
ProfessorAI is a Streamlit application designed to help users explore various aspects of professors' teaching styles, courses, and academic contributions. By selecting a professor from a predefined list, users can ask specific questions and retrieve answers based on processed data. This application integrates with external sources and uses natural language processing to provide insights.

#### Features
- **Professor Selection**: Users can choose from a dropdown list of professors, which are mapped to their unique identifiers.
- **Dynamic Information Retrieval**: Upon selecting a professor and asking a question, the app fetches and processes relevant data to generate an answer.
- **Source Linking**: Each answer is accompanied by a link to the source, ensuring transparency and the ability to verify information.

#### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/AkankshaReddyP/ProfessorAI.git
   ```
2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

#### Usage
1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```
2. **Navigate to the local server URL** displayed in your terminal (usually http://localhost:8501).

3. **Select a professor from the dropdown menu** and click "Process Professor" to load their data.

4. **Enter a question in the text box** to inquire about the selected professor.

#### How it Works
- The app uses the `requests` library to fetch professor-related data from external sources.
- `BeautifulSoup` is employed to parse HTML content and extract relevant information.
- `langchain` and `OpenAI` APIs are integrated for natural language processing and to generate embeddings.
- Data is processed and stored using the `FAISS` vector store for quick retrieval.

#### Screenshot
Below is a screenshot of the app's interface showing an example of its functionality:
<img width="960" alt="image" src="https://github.com/user-attachments/assets/b1959067-2535-422f-a385-725cead3dbfa">

