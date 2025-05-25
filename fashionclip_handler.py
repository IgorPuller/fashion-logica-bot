from fashion_clip.fashion_clip import FashionCLIP
from PIL import Image
import torch
import torch.nn.functional as F

model = FashionCLIP('fashion-clip')

def process_photo(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")

    labels = [
        "повседневный стиль",
        "деловая одежда",
        "вечернее платье",
        "спортивный образ",
        "мужской уличный стиль",
        "женский уличный стиль",
        "классический стиль",
        "яркий наряд",
        "минимализм",
        "стиль бохо"
    ]

    # Получаем numpy → конвертируем в torch
    image_features = torch.tensor(model.encode_images([image], batch_size=1))
    text_features = torch.tensor(model.encode_text(labels, batch_size=len(labels)))

    # Нормализуем
    image_features = F.normalize(image_features, p=2, dim=1)
    text_features = F.normalize(text_features, p=2, dim=1)

    # Косинусное сходство
    similarities = image_features @ text_features.T
    best_idx = torch.argmax(similarities).item()
    best_score = similarities[0, best_idx].item()

    return f"{labels[best_idx]} (уверенность: {best_score:.2f})"



