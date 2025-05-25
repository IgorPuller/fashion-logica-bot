from fashion_clip.fashion_clip import FashionCLIP
from PIL import Image
import torch
from yandex_gpt import ask_yandex_gpt  

model = FashionCLIP('fashion-clip')

def process_photo(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")
    
    # Получаем эмбеддинг и превращаем в список
    embedding = model.encode_images([image], batch_size=1)
    vector = embedding[0].tolist()
    
    # Обрезаем и округляем до 100 значений для компактности
    vector_short = [round(x, 4) for x in vector[:100]]

    # Создаём промпт
    prompt = (
                "На этом фото изображена одежда. Опиши, какой у неё стиль. "
                "Не используй фразы вроде 'я думаю' или 'этот вектор'. "
                "Говори развернуто,уверенно, как стилист, аргументируй свой ответ. "
                "Начни с фразы: 'На этом фото ...'\n\n"
                f"Вектор признаков: {vector_short}"
            )

    # Отправляем запрос в YandexGPT
    style = ask_yandex_gpt(prompt)

    return f"🧠 {style}"




