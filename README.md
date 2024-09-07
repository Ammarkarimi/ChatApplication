# Techbot Chat Application

This project is a chatbot application built using [Flet](https://flet.dev/) for the UI, [LangChain](https://github.com/hwchase17/langchain) for prompt handling, and [CTransformers](https://github.com/QwenLM/langchain-community-ctfs) for invoking an LLaMA model to provide responses. The chatbot allows users to ask relevant questions and receive AI-generated responses.

## Features

- **Splash Screen**: Displays a welcome message before loading the main interface.
- **Instruction Page**: Provides guidelines for interacting with the chatbot. Users must agree to the terms and conditions to proceed to the chat.
- **Chat Interface**: Users can enter a name, ask questions, and receive precise responses from the chatbot.
- **Message Auto-scroll**: Chat messages automatically scroll to the latest message.
- **Flet-based UI**: Interactive, responsive user interface for web-based applications.

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- `torch` (PyTorch)
- `flet` (for the user interface)
- `langchain` (for handling prompt templates)
- `langchain_community.llms.CTransformers` (for LLaMA model integration)

### Install Dependencies

Install the required dependencies using pip:

```bash
pip install torch flet langchain langchain_community.ctfs
```
### LLaMA Model
Download the LLaMA model (or any supported model) and place it in the correct directory. Update the path in the CTransformers model configuration in the code:

```bash
llm = CTransformers(model='.\\model\\llama-2-7b-chat.ggmlv3.q8_0.bin', ...)
```
Ensure you have the model file in the correct location.

### Running the Application
To run the chatbot, execute the following command:

```bash
python app.py
```
The application will start and be served on your browser. The splash screen will be displayed for 3 seconds, followed by the instructions page. After agreeing to the terms and conditions, users can join the chat interface.

## Usage
 - Splash Screen: Wait for the splash screen to disappear.
 - Instruction Page: Read the instructions and agree to the terms to proceed.
 - Chat Interface: Enter your name and start chatting with the bot.
 - Asking Questions: The bot answers only relevant, well-phrased questions. Avoid vague or inappropriate queries.

## Code Overview
- Splash Screen: splash_screen(page) shows a welcome message for 3 seconds.
- Instruction Page: instruction_page(page) provides interaction guidelines and a checkbox for agreeing to the terms.
- Main Chat Interface: main_chat_interface(page) handles user input, sends questions to the chatbot, and displays responses.
= Chatbot Logic: Uses CTransformers with an LLaMA model to generate responses based on user queries.

## Key Functions
- splash_screen(page): Displays a splash screen with a welcome message.
- instruction_page(page): Displays instructions for using the chatbot and collects user agreement.
- main_chat_interface(page): Main chat interface where users can interact with the chatbot.
- bot(message): Processes user input and generates a response using the LLaMA model.

## Customization
You can modfiy Llama model or use a different model by modifying the CTransformers configuration:
```bash
llm = CTransformers(
    model='path_to_your_model.bin',
    model_type='llama',
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
    config={'temperature': 0.7}
)
```

## UI Customization
You can modify the colors, fonts, and layout by editing the relevant parts of the UI code. For example, to change the background color of the chat interface, update the bgcolor attribute in ft.Container.

## Notes:
1. Ensure you update the model path in the instructions as per your setup.
2. Provide any additional instructions relevant to your specific deployment or usage scenario.



