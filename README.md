# Population LlamaIndex Query Assistant 🚀

Welcome to the **Population LlamaIndex Query Assistant**! 🌍 This project uses **LlamaIndex** (formerly GPT Index) along with **MistralAI** and **Langfuse** to provide a powerful query assistant for population and country-related data, leveraging natural language processing for seamless interaction. 🧠💡

### Features ✨
- 🗺️ Query population data from a CSV file.
- 🇨🇦 Retrieve detailed information about Canada using PDF data.
- 📝 Save notes and interact with various data sources using LlamaIndex.
- 🔌 Easily interact with a ReAct-based agent for versatile querying.

### Getting Started 🛠️

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ChahineBA/POPULATION-LLAMAINDEX-QUERY-ASSISTANT.git
   cd POPULATION-LLAMAINDEX-QUERY-ASSISTANT
   ```
2. **Install dependencies:**
   First, install all the dependencies using requirements.txt.
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   Create a .env file in the root of the project with the following keys:
   ```bash
   MISTRAL_API_KEY=your_mistral_api_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
4. **Run the app**:
   Start the app with Streamlit:
   ```bash
   streamlit run main.py
   ```
### Notes 📌
- Ensure you have the correct API keys in your .env file for Mistral and Langfuse.
- - [MistralAI API Key](https://mistral.ai/docs/) 
  - [Langfuse API Key](https://docs.langfuse.com/) 
- The project is designed to provide interactive querying via Streamlit, making it easy to explore data about populations and countries.
