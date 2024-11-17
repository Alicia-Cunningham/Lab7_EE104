import gradio as gr
import openai
import docx2txt
import PyPDF2


# Set OpenAI API key securely (replace "YOUR_API_KEY" with your actual key)
openai.api_key = "apikey"  # Replace with your key if not using an environment variable

# Function to read text from file
def read_text_from_file(file_path):
    text = ""
    if file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''.join(page.extract_text() for page in pdf_reader.pages)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            text = txt_file.read()
    print("File content extracted:")  # Debugging: show first 100 chars
    return text

def bot(history, filename=None):
    # Initialize the OpenAI formatted conversation history
    history_openai_format = []

    # Add file contents to the conversation history if a file is uploaded
    if filename:
        for file in filename:
            file_contents = read_text_from_file(file.name)
            history_openai_format.append({"role": "user", "content": file_contents})

    # Convert Gradio chat history to OpenAI format
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        if assistant is not None:
            history_openai_format.append({"role": "assistant", "content": assistant})

    # Attempt the OpenAI API call with debugging
    try:
        print("History formatted for OpenAI:", history_openai_format)  # Debugging
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=history_openai_format,
            stream=True
        )

        # Process and yield each chunk from the response
        history[-1][1] = ""  # Initialize bot response in history
        for chunk in response:
            text = chunk.choices[0].delta.get("content", "")
            history[-1][1] += text
            yield history

    except openai.error.AuthenticationError:
        print("Authentication Error: Check your API key.")
        history[-1][1] = "There was an issue with the API key."
        yield history
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        history[-1][1] = "An unexpected error occurred. Please check the console for more details."
        yield history

def user(user_message, history):
    print("User message received:", user_message)  # Debugging
    return "", history + [[user_message, None]]

custom_css = """

    body { background-color: #0033A0; }   /* SJSU blue background */
    h1, h2, h3, h4 { color: #F1A100; border: 1px solid #0033A0}    /* SJSU yellow for headers */
     button { background-color: #0033A0 !important; color: white !important; border: 2px solid #F1A100 !important; } /* Button styling */
    .gr-text-input textarea { border: 2px solid #F1A100 !important; color: white !important; } /* Textbox border and text color */
    .gr-file input[type='file'] { border: 2px solid #F1A100 !important; color: white !important; } /* File input border and text color */

"""

# Setting up Gradio Blocks
with gr.Blocks(css=custom_css) as demo:

    gr.Markdown("## SJSU EE104 - Upload Your File and Ask Questions")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...", label="Ask A Question:")
    clear = gr.Button("Clear")
    filename = gr.File(file_count='multiple')

    # User input submission
    msg.submit(
        fn=user, inputs=[msg, chatbot], outputs=[msg, chatbot]
    ).then(
        fn=bot, inputs=[chatbot, filename], outputs=chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

# Launch the Gradio app
demo.queue()
demo.launch()
