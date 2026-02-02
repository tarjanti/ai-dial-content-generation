import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._models.message import Message
from task._models.role import Role
from task._utils.bucket_client import DialBucketClient
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    async with DialBucketClient(API_KEY, DIAL_URL) as dial_bucket_client:
        file_content = None
        with open(image_path, "rb") as image_file_handle:
            file_content = image_file_handle.read()
        image_content = BytesIO(file_content)

        response_as_dict = await dial_bucket_client.put_file(file_name, mime_type_png, image_content)

        return Attachment(title=file_name, url=response_as_dict.get("url"), type=mime_type_png)


def start() -> None:
    dial_model_client = DialModelClient(DIAL_CHAT_COMPLETIONS_ENDPOINT, "gpt-4o", API_KEY)

    attachment = asyncio.run(_put_image())
    print(f"attachment: {attachment}")

    message = Message(Role.USER, "What do you see on this picture?", CustomContent([attachment]))

    ai_message = dial_model_client.get_completion([message])
    print(f"AI: {ai_message}")


start()
