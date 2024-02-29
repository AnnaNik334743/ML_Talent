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