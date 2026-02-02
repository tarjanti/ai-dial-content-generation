import asyncio

from task._models.custom_content import Attachment
from task._models.message import Message
from task._models.role import Role
from task._utils.bucket_client import DialBucketClient
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient


class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"


async def _save_images(attachments: list[Attachment]):
    async with DialBucketClient(API_KEY, DIAL_URL) as dial_bucket_client:
        for attachment in attachments:
            if attachment.type and attachment.type == 'image/png':
                image_bytes = await dial_bucket_client.get_file(attachment.url)
                image_file_name = f"{attachment.title}.png"
                with open(image_file_name, "wb") as image_file_handle:
                    image_file_handle.write(image_bytes)
                print(f"Image saved into file: {image_file_name}")


def start() -> None:
    dial_model_client = DialModelClient(DIAL_CHAT_COMPLETIONS_ENDPOINT, "dall-e-3", API_KEY)

    message = Message(Role.USER, 'Generate image for "Sunny day on Bali"')

    ai_message = dial_model_client.get_completion([message], custom_fields={
        "size": Size.square,
        "style": Style.vivid,
        "quality": Quality.standard,
    })

    if custom_content := ai_message.custom_content:
        if attachments := custom_content.attachments:
            asyncio.run(_save_images(attachments))


start()
