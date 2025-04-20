from pydantic_ai.models import Model
from openai import OpenAI

from src.application.agents.image_gen import prompt
from src.infrastructure.config import config


class ImageGenerator:
    def __init__(self):
        self.__model_name = config.OPENAI_IMAGE_GEN_MODEL_NAME
        self.__api_key = config.OPENAI_API_KEY.get_secret_value()
        self.__client = self.__create_client()

    def __create_client(self) -> OpenAI:
        """
        Create an client for image generation
        """
        return OpenAI(api_key=self.__api_key)

    async def execute(self, topic: str):
        """
        Generates image
        """
        image_prompt = prompt.replace("{{topic}}", topic)
        try:
            result = self.__client.images.generate(
                model=self.__model_name,  # dall-e-3
                prompt=image_prompt,
                size="1024x1024",
                quality="hd",
                n=1,
            )
            return result.data[0].url
        except Exception as e:
            return None
