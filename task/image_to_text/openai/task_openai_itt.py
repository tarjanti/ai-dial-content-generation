import base64
from pathlib import Path

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    dial_model_client = DialModelClient(DIAL_CHAT_COMPLETIONS_ENDPOINT, "gpt-4o", API_KEY)

    prompt_content = TxtContent("What is in the image?")

    image_content_for_base64_encoded_image = ImgContent(ImgUrl(f"data:image/png;base64,{base64_image}"))
    message_with_base64_encoded_image = ContentedMessage(Role.USER, [prompt_content, image_content_for_base64_encoded_image])
    ai_message_for_base64_encoded_image = dial_model_client.get_completion([message_with_base64_encoded_image])
    print("AI: response: " + str(ai_message_for_base64_encoded_image))

    image_content_for_image_url = ImgContent(ImgUrl("https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg"))
    message_with_image_url = ContentedMessage(Role.USER, [prompt_content, image_content_for_image_url])
    ai_message_for_image_url = dial_model_client.get_completion([message_with_image_url])
    print("AI: response: " + str(ai_message_for_image_url))

start()
