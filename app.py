import flet as ft
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import torch  # Ensure torch is imported
import time
import threading

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def splash_screen(page: ft.Page):
    splash = ft.Container(
        content=ft.Text("Welcome to Techbot!", size=40, color=ft.colors.AMBER_50),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK87,
        expand=True
    )

    page.add(splash)

    def remove_splash_screen():
        time.sleep(10)  # Show the splash screen for 3 seconds
        page.clean()  # Remove splash screen
        instruction_page(page)  # Load instruction page

    # Run the splash screen removal in a separate thread
    threading.Thread(target=remove_splash_screen).start()


def instruction_page(page: ft.Page):
    def proceed_to_chat(e):
        if agree_checkbox.value:
            page.clean()  # Remove the instruction page
            main_chat_interface(page)  # Proceed to chat interface
        else:
            agree_checkbox.error_text = "You must agree to continue."
            agree_checkbox.update()

    agree_checkbox = ft.Checkbox(label="I agree to the Terms and Conditions")

    # Instructions content
    instructions = ft.Column([
        ft.Text("Instructions", size=30, weight="bold", color=ft.colors.AMBER_50),
        ft.Text("Welcome to the chatbot! To ensure a smooth and productive interaction, it’s important to follow these guidelines when asking questions. The chatbot is designed to assist you in the best possible way, but it relies on clear and specific inputs from you.", size=18, color=ft.colors.AMBER_50),
        ft.Text("When asking questions, always aim to be as clear and concise as possible. The chatbot processes your queries based on the information provided, so vague or unclear questions may result in inaccurate or incomplete responses. For example, instead of asking something broad like “Tell me everything about technology,” you can ask more focused questions like “What are the latest advancements in artificial intelligence?” This helps the bot generate a precise and relevant answer.", size=16, color=ft.colors.AMBER_50),
        ft.Text("It’s important to remember that the chatbot is here to help with factual information and assistance on a wide range of topics, but it cannot respond to inappropriate, offensive, or irrelevant queries. Please ensure that your questions are respectful and appropriate for the platform. The chatbot is a tool for productive interaction, and following these guidelines will help you get the most out of your experience.", size=16, color=ft.colors.AMBER_50),
        ft.Text("If you’re unsure about how to phrase a question, think about what specific information you’re looking for. A well-phrased question is likely to receive a well-phrased response. For instance, instead of asking “What is AI?” you could ask “Can you explain how AI is used in healthcare?” This will give you more relevant and detailed information in return.", size=16, color=ft.colors.AMBER_50),
        ft.Text("Additionally, keep your questions as brief as possible while still being informative. Long-winded or overly complex questions may confuse the chatbot and lead to responses that are not fully aligned with your expectations. By keeping your questions short and to the point, you can expect quicker and more accurate responses.", size=16, color=ft.colors.AMBER_50),
        ft.Text("Finally, remember that the chatbot is here to assist you, so feel free to ask as many relevant questions as you need. However, refrain from submitting multiple unrelated queries in one go, as this might overwhelm the system and lead to mixed or inaccurate answers. It's best to ask one question at a time, wait for a response, and then proceed with your next inquiry.", size=16, color=ft.colors.AMBER_50),
        ft.Text("By following these guidelines, you’ll have a smoother and more productive interaction with the chatbot. The more relevant your questions, the better the chatbot will be able to assist you. Enjoy the experience, and don’t hesitate to ask if you need help!", size=16, color=ft.colors.AMBER_50),
        agree_checkbox,
        ft.ElevatedButton("Proceed", on_click=proceed_to_chat, width=200,color=ft.colors.AMBER_50),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    # Add the instruction page content with scrolling enabled
    page.add(
        ft.Container(
            content=ft.Column(
                [instructions],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO  # Enable scrolling
            ),
            alignment=ft.alignment.center,
            padding=20,
            expand=True,
            bgcolor=ft.colors.BLACK87,  # Background color for contrast
        )
    )


def main_chat_interface(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Techbot"

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value,
                                         text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get(
                "user_name"), new_message.value, message_type="chat_message"))
            temp = new_message.value
            new_message.value = ""
            new_message.focus()
            res = bot(temp)
            if len(res) > 220:  # adjust the maximum length as needed
                res = '\n'.join([res[i:i+220]
                                for i in range(0, len(res), 220)])
            page.pubsub.send_all(
                Message("Techbot", res, message_type="chat_message"))
            page.update()

    def bot(message):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        llm = CTransformers(model='.\\model\\llama-2-7b-chat.ggmlv3.q8_0.bin',
                            model_type='llama',
                            device=device,
                            config={
                                'temperature': 0.7,
                            })

        template = """
        You are a chatbot and you need to give precise answers to the user queries. Just give the answer and avoid unnecessary information.
        Query: {message}
        Answer: 
        """

        prompt = PromptTemplate(input_variables=['message'],
                                template=template)

        response = llm.invoke(prompt.format(message=message))
        return response

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True,
                        color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(
            text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,  # Enable auto-scroll in the chat list
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


def main(page: ft.Page):
    splash_screen(page)

ft.app(target=main)
