import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file.docs import PDFReader
from llama_index.core import Settings

# Function to get an index for querying based on the provided data
def get_index(data, index_name, llm, embed_model):
    index = None
    
    # Set the LLM (Large Language Model) and embed_model in the global Settings object
    # This will ensure that the provided models are used during index creation
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    # Set chunk size for processing documents; this will control the maximum size of each chunk of data processed
    Settings.chunk_size = 512

    # Check if the index already exists in the specified directory
    if not os.path.exists(index_name):
        print("Building index", index_name)  # Indicate that the index is being built

        # If the index does not exist, create a new VectorStoreIndex from the provided documents (data)
        index = VectorStoreIndex.from_documents(data, show_progress=True)

        # Persist the created index to the specified directory so it can be reused in the future
        index.storage_context.persist(persist_dir=index_name)
    else:
        # If the index exists, load it from the storage context (existing index)
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )
    
    return index

# Function to create a query engine for the Canada PDF document
def create_canada_engine(llm, embed_model):
    """Creates a query engine for the Canada PDF."""
    
    # Define the path to the Canada PDF file
    pdf_path = os.path.join("data", "Canada.pdf")
    
    # Check if the PDF file exists at the given path
    if not os.path.exists(pdf_path):
        # If the file is not found, raise a FileNotFoundError
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # Load the content of the Canada PDF using the PDFReader
    canada_pdf = PDFReader().load_data(file=pdf_path)
    
    # Generate the index for the loaded PDF data, passing in the LLM and embedding model
    canada_index = get_index(canada_pdf, "canada", llm, embed_model)
    
    # Return the query engine for the Canada index, allowing queries to be made against the PDF data
    return canada_index.as_query_engine()
