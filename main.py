# Load environment variables from a .env file
from dotenv import load_dotenv  # Import to load environment variables from a .env file
import os  # Import the os module for accessing environment variables and file paths
import pandas as pd  # Import pandas for handling and querying dataframes
import streamlit as st
# Import the PandasQueryEngine for querying Pandas DataFrames
from llama_index.experimental.query_engine import PandasQueryEngine

# Import custom prompt templates
from prompts import new_prompt, instruction_str, context  # Import custom prompt templates for querying

# Allow asynchronous code to run in environments that normally block it
import nest_asyncio  # Import nest_asyncio to allow running async code in environments like Jupyter

# Import and set up the Llama Index with MistralAI components
from llama_index.llms.mistralai import MistralAI  # Import MistralAI LLM model for advanced language processing
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Import HuggingFaceEmbedding for embeddings
from llama_index.core import Settings  # Import Settings to configure global settings for Llama Index

# Import Langfuse for logging and callbacks
from langfuse import Langfuse  # Langfuse for event tracking and debugging
from llama_index.core.callbacks import CallbackManager  # Import callback manager for handling events
from langfuse.llama_index import LlamaIndexCallbackHandler  # Langfuse callback handler specifically for Llama Index

# Import note engine for saving user-generated notes
from note_engine import note_engine

# Import tools for querying and interacting with data and agents
from llama_index.core.agent import ReActAgent  # ReAct agent for reactive agents that can perform multiple tasks
from llama_index.core.tools import QueryEngineTool, ToolMetadata  # Import tools for query engines and tool metadata

# Import PDF engine for querying the Canada PDF document
from pdf import create_canada_engine

# Load the .env file to access environment variables
load_dotenv()  # Loads variables from a .env file (if present)

# Apply the nest_asyncio patch to enable running asynchronous loops
nest_asyncio.apply()  # Allows async code execution in environments like Jupyter

# Retrieve the Mistral API key from the environment variables
os.getenv("MISTRAL_API_KEY")  # Get the Mistral API key from the environment variables for authentication

# Define the large language model (LLM) with specific configurations
llm = MistralAI(model="open-mixtral-8x22b", temperature=0.1)  # Set the LLM (Mistral) with a specific temperature

# Define the embedding model for vector-based representations
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")  # Set embedding model for embedding-based tasks

# Set the LLM and embedding model globally in the Settings object
Settings.llm = llm  # Set the LLM in the global settings
Settings.embed_model = embed_model  # Set the embedding model in the global settings

# Initialize Langfuse for logging and debugging, using keys from environment variables
langfuse = Langfuse(
  secret_key=os.environ["LANGFUSE_SECRET_KEY"],  # Get the secret key for Langfuse from environment variables
  public_key=os.environ["LANGFUSE_PUBLIC_KEY"],  # Get the public key for Langfuse
  host=os.environ["LANGFUSE_HOST"]  # Get the Langfuse host URL
)

# Set up the Langfuse callback handler for Llama Index
langfuse_callback_handler = LlamaIndexCallbackHandler()  # Initialize the callback handler for Llama Index

# Add the callback handler to the Settings callback manager
Settings.callback_manager = CallbackManager([langfuse_callback_handler])  # Attach the callback handler to the global settings

# Define the path to the population dataset
population_path = os.path.join("data", "population.csv")  # Path to the population dataset

# Load the population dataset into a Pandas DataFrame
population_df = pd.read_csv(population_path)  # Read the CSV file into a DataFrame

# Initialize a PandasQueryEngine for querying the population DataFrame
population_query_engine = PandasQueryEngine(
    df=population_df,  # Set the dataframe to query
    verbose=True,  # Enable detailed output for queries
    instruction_str=instruction_str,  # Provide custom instructions for query handling
)

# Update the query engine with a new custom prompt
population_query_engine.update_prompts({"pandas_prompt": new_prompt})  # Update the query engine with a custom prompt template

# Initialize the Canada query engine using the custom PDF engine
canada_engine = create_canada_engine(llm, embed_model)  # Create a query engine for Canada-related queries

# Define a list of tools (including note engine and query engines)
tools = [
    note_engine,  # Note engine to save user-generated notes
    QueryEngineTool(query_engine=population_query_engine, metadata=ToolMetadata(  # Tool for querying population data
        name="population_data",  # Tool name for population data queries
        description="this gives information at the world population and demographics"  # Description of the tool
    )),
    QueryEngineTool(  # Tool for querying Canada-related data
        query_engine=canada_engine,
        metadata=ToolMetadata(
            name="canada_data",  # Tool name for Canada data queries
            description="this gives detailed information about canada the country"  # Description of the tool
        )
    )
]

# Initialize a ReAct agent with the tools and context
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)  # Create an agent that reacts to user input

# Streamlit app
def main():
    # Title of the app
    st.title("Llama Index Query Assistant")

    # User input for the prompt
    prompt = st.text_input("Enter your query (type 'q' to quit):")
    result=""
    if prompt.lower() == "q":
        st.write("Goodbye!")
        return
    # Query the agent with the user's input
    if prompt:
        with st.spinner("Processing your query..."):
            result = agent.query(prompt)  # Get the result from the agent
            st.write("Result:")
            st.write(result.response)
    
    # Option to save notes
    
    if st.button("Save this result as a note"):
        prompt = ('save this note for me' + result.response)
        result = agent.query(prompt)
        if result:
            st.success("Note saved successfully!")
        else:
            st.error("Error While Saving Note")

if __name__ == "__main__":
    main()
