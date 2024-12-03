from llama_index.core.tools import FunctionTool  # Import FunctionTool from llama_index to define custom tools
import os  # Import os module to handle file paths and file system operations

# Define the path to the notes file where the notes will be saved
note_file = os.path.join("data", "notes.txt")

# Function to save a note to the file
def save_note(note):
    # Check if the notes file exists, if not, create it
    if not os.path.exists(note_file):
        # Open the file in write mode, which will create the file if it doesn't exist
        open(note_file, "w")

    # Open the file in append mode to add the note at the end of the file
    with open(note_file, "a") as f:
        # Write the note to the file, adding a newline character after each note
        f.writelines([note + "\n"])

    # Return a success message indicating that the note was saved
    return 'note saved'

# Create a FunctionTool using the save_note function
note_engine = FunctionTool.from_defaults(
    fn=save_note,  # Pass the function to be used by the tool
    name="note_saver",  # Provide a name for the tool
    description="this tool can save a text-based note to a file for the user"  # Description of what the tool does
)
