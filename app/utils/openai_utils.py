from openai import OpenAI  # Imports the new OpenAI SDK client class
import os  

# Set your API key from environment variable (best practice for security)
OpenAI.api_key = os.environ.get("OPENAI_API_KEY")

# Function to generate payment steps using OpenAI's ChatGPT model
def generate_steps_from_text(extracted_text, vendor):
    # Create a user prompt to describe what we want GPT to do
    prompt = (
        f"The following is an OCR extraction from a utility bill for '{vendor}'.\n\n"
        f"Document:\n{extracted_text}\n\n"
        "Based on this, provide clear, numbered step-by-step payment instructions a user can follow to pay their bill online."
    )

    # Initialize OpenAI client
    client = OpenAI()

    # Send a chat completion request to GPT-3.5
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ChatGPT model to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes payment instructions."},  # Sets the assistant's behavior
            {"role": "user", "content": prompt}  # Supplies the prompt asking for steps based on OCR output
        ]
    )

    # Extract the text content of the assistant's response
    output = response.choices[0].message.content
    print(output)  # Optional: log to console for debugging

    return output  # Return the raw string from GPT (e.g., "1. Go to site\n2. Log in...")

# 🧹 Helper function to parse GPT response into a clean list of steps
def parse_steps(raw_text):
    # Split the text by line breaks and remove any extra whitespace
    lines = raw_text.strip().split("\n")
    steps = [line.strip() for line in lines if line.strip()]  # Filters out any empty lines

    return steps  # Returns: ["1. Do X", "2. Do Y", ...]
