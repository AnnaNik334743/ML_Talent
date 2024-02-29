nums_to_english = {"contact_type": {1: "Phone", 2: "Email", 3: "Skype", 4: "Telegram", 5: "Github"},
                   "education_type": {1: "Elementary", 2: "Training", 3: "Sertificates", 4: "Basic"},
                   "education_level": {1: "Secondary", 2: "Secondary professional", 3: "Higher incomplete", 4: "Higher",
                                       5: "Bachelor", 6: "Master", 7: "Phd", 8: "Doctor"},
                   "language_level": {1: "Beginning", 2: "Pre-intermediate", 3: "Intermediate", 4: "Upper-intermediate",
                                      5: "Advanced", 6: "Proficient", 7: "Nativ"}}

english_to_nums = {"contact_type": {value: key for key, value in nums_to_english["contact_type"].items()},
                   "education_type": {value: key for key, value in nums_to_english["education_type"].items()},
                   "education_level": {value: key for key, value in nums_to_english["education_level"].items()},
                   "language_level": {value: key for key, value in nums_to_english["language_level"].items()}}

nums_to_russian = {"contact_type": {1: "Телефон", 2: "Email", 3: "Skype", 4: "Telegram", 5: "Github"},
                   "education_type": {1: "Начальное", 2: "Повышение квалификации", 3: "Сертификаты", 4: "Основное"},
                   "education_level": {1: "Среднее", 2: "Среднее специальное", 3: "Неоконченное высшее", 4: "Высшее",
                                       5: "Бакалавр", 6: "Магистр", 7: "Кандидат наук", 8: "Доктор наук"},
                   "language_level": {1: "Начальный", 2: "Элементарный", 3: "Средний", 4: "Средне-продвинутый",
                                      5: "Продвинутый", 6: "В совершенстве", 7: "Родной"}}

russian_to_nums = {"contact_type": {value: key for key, value in nums_to_russian["contact_type"].items()},
                   "education_type": {value: key for key, value in nums_to_russian["education_type"].items()},
                   "education_level": {value: key for key, value in nums_to_russian["education_level"].items()},
                   "language_level": {value: key for key, value in nums_to_russian["language_level"].items()}}


def postprocess_special_fields(d):
    language = d['resume']['language']
    if language == 'en':
        values = english_to_nums
    elif language == 'ru':
        values = russian_to_nums
    else:
        raise Exception('unknown language')
    for i in range(len(d["resume"]["contactItems"])):
        d["resume"]["contactItems"][i]["contact_type"] = values["contact_type"].get(
            d["resume"]["contactItems"][i]["contact_type"], '')
    for i in range(len(d["resume"]["educationItems"])):
        d["resume"]["educationItems"][i]["education_type"] = values["education_type"].get(
            d["resume"]["educationItems"][i]["education_type"], '')
        d["resume"]["educationItems"][i]["education_level"] = values["education_level"].get(
            d["resume"]["educationItems"][i]["education_level"], '')
    for i in range(len(d["resume"]["languageItems"])):
        d["resume"]["languageItems"][i]["language_level"] = values["language_level"].get(
            d["resume"]["languageItems"][i]["language_level"], '')
    return d
