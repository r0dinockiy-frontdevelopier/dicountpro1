import asyncio
import aiohttp
from django.conf import settings

async def ask_yandex_gpt_async(prompt: str) -> str | None:
    """
    Асинхронно отправляет запрос к YandexGPT и возвращает ответ.
    """
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_GPT_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "modelUri": f"gpt://{settings.YANDEX_GPT_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": 500
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты - ИИ-ассистент компании DiscountPRO, которая занимается системами управления дисконтными программами. Отвечай вежливо и по делу."
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            if response.status == 200:
                result = await response.json()
                return result['result']['alternatives'][0]['message']['text']
            else:
                error_text = await response.text()
                print(f"Ошибка YandexGPT: {response.status} - {error_text}")
                return None

def ask_yandex_gpt(prompt: str) -> str | None:
    """Синхронная обёртка для вызова из Django-представлений"""
    return asyncio.run(ask_yandex_gpt_async(prompt))