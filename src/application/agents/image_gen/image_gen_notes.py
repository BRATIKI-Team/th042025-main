from pydantic_ai.models import Model
import asyncio
from openai import OpenAI


class ImageGenerator:
    def __init__(self, llm: Model, api_key: str):
        self.__llm = llm
        self.__api_key = api_key
        self.__client = self.__create_client()

    def __create_client(self) -> OpenAI:
        """
        Create an client for image generation
        """
        return OpenAI(api_key=self.__api_key)

    async def execute(self, image_prompt: str) -> str:
        """
        Generates image
        """
        result = self.__client.images.generate(
            model=self.__llm,  # dall-e-3
            prompt=image_prompt,
            size="1024x1024",
            quality="hd",  # standart 12 sec, hd 18 sec
            n=1,
            # response_format="b64_json" #url - url, b64_json ����� ���� �����
        )
        return result.data[0].url


gen = ImageGenerator("dall-e-3", "your_api_key")  # api key in DI


imag = asyncio.run(gen.execute("cat in space"))


print(imag)
