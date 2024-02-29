from typing import Any
from PIL import Image


def naive_lang_detect(text: str) -> str:
    """
    Detects the language of the text (Russian or English) based on the frequency of language-specific letters.

    Parameters:
        text (str): The input text to be analyzed.

    Returns:
        str: 'en' if the text is primarily in English, 'ru' if the text is primarily in Russian.
    """
    english_letters = 0
    russian_letters = 0

    for char in text:
        if char.isalpha() and char.isascii():
            english_letters += 1
        elif char.isalpha() and not char.isascii():
            russian_letters += 1

    return 'en' if english_letters > russian_letters else 'ru'


def is_human(img: Image.Image, model: Any) -> bool:
    """
    Detects whether there is a human in an image using an object detection model.

    Parameters:
        img (PIL.Image.Image): The image to be analyzed.
        model (any): The object detection model.

    Returns:
        bool: True if a human is detected in the image, False otherwise.
    """
    output = model(img, verbose=False)
    res = output[0]
    classes = res.boxes.cls
    probs = res.boxes.conf
    for p, c in zip(probs, classes):
        if c.item() == 0 and p.item() > 0.3:
            return True
    return False
