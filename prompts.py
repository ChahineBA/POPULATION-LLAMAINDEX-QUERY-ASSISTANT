from llama_index.core import PromptTemplate  # Import PromptTemplate from llama_index for creating prompts

# Define the instruction string that outlines the steps the agent should follow
instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""

# Create a new prompt template using the instructions and input placeholders
new_prompt = PromptTemplate(
    """\
    You are working with a pandas dataframe in Python.
    The name of the dataframe is `df`.
    This is the result of `print(df.head())`:
    {df_str}  # Placeholder for the dataframe preview

    Follow these instructions:
    {instruction_str}  # The instructions to convert the query to executable code
    Query: {query_str}  # The user's query

    Expression: """  # This part is where the Python code expression will be returned
)

# Contextual information about the agent's role
context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about world population statistics and details about a country. """
