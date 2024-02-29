ENGLISH_PROMPT = """
Extract information about candidate from this raw CV text. Return your answer in json format like this:
```
{
  "resume": {
      "resume_id": "",
      "first_name": "",
      "last_name": "",
      "middle_name": "",
      "birth_date": "",
      "birth_date_year_only": "",
      "country": "",
      "city": "",
      "about": "",
      "key_skills": "",
      "salary_expectations_amount": "",
      "salary_expectations_currency": "",
      "photo_path": "",
      "gender": "",
      "language": "",
      "resume_name": "",
      "source_link": "",
      "contactItems": [
        {
          "resume_contact_item_id": "",
          "value": "",
          "comment": "",
          "contact_type": ""
        }
      ],
      "educationItems": [
        {
          "resume_education_item_id": "",
          "year": "",
          "organization": "",
          "faculty": "",
          "specialty": "",
          "result": "",
          "education_type": "",
          "education_level": ""
        }
      ],
      "experienceItems": [
        {
          "resume_experience_item_id": "",
          "starts": "",
          "ends": "",
          "employer": "",
          "city": "",
          "url": "",
          "position": "",
          "description": "",
          "order": ""
        }
      ],
      "languageItems": [
        {
          "resume_language_item_id": "",
          "language": "",
          "language_level": ""
        }
      ]
    }
}
```
Do not create any extra fields. Answer in English. Consider this information and use numbers in these fields:
```
1.  contact_type: {
    1: Phone
    2: Email
    3: Skype
    4: Telegram
    5: Github
}
Often contacts are written in the beginning of a CV.

2. education_type: {
    1: Elementary
    2: Training
    3: Sertificates
    4: Basic

}
This is usually about schools and courses of a candidate.

3. education_level: {
    1: Secondary
    2: Secondary professional
    3: Higher incomplete
    4: Higher
    5: Bachelor
    6: Master
    7: PhD
    8: Doctor
}
This field is usually about schools and courses of a candidate.

3. language_level: {
    1: Beginning
    2: Pre-intermediate
    3: Intermediate
    4: Upper-intermediate
    5: Advanced
    6: Proficient
    7: Native
}
Sometimes candidates specify language_level information, but not always. 
```
"""


RUSSIAN_PROMPT = """
Извлеки информацию о кандидате из этого текста резюме. Верни ответ в json формате следующего вида:
```
{
  "resume": {
      "resume_id": "",
      "first_name": "",
      "last_name": "",
      "middle_name": "",
      "birth_date": "",
      "birth_date_year_only": "",
      "country": "",
      "city": "",
      "about": "",
      "key_skills": "",
      "salary_expectations_amount": "",
      "salary_expectations_currency": "",
      "photo_path": "",
      "gender": "",
      "language": "",
      "resume_name": "",
      "source_link": "",
      "contactItems": [
        {
          "resume_contact_item_id": "",
          "value": "",
          "comment": "",
          "contact_type": ""
        }
      ],
      "educationItems": [
        {
          "resume_education_item_id": "",
          "year": "",
          "organization": "",
          "faculty": "",
          "specialty": "",
          "result": "",
          "education_type": "",
          "education_level": ""
        }
      ],
      "experienceItems": [
        {
          "resume_experience_item_id": "",
          "starts": "",
          "ends": "",
          "employer": "",
          "city": "",
          "url": "",
          "position": "",
          "description": "",
          "order": ""
        }
      ],
      "languageItems": [
        {
          "resume_language_item_id": "",
          "language": "",
          "language_level": ""
        }
      ]
    }
}
```
Не придумывай лишних полей. Отвечай на русском. Учитывай следующую информацию и используй нужные номера в этих полях:
```
1. Типы контактов — contact_type: {
    1: Телефон
    2: Email
    3: Skype
    4: Telegram
    5: Github
}
Часто контакты указаны в начале резюме.

2. Виды образования — education_type: {
    1: Начальное
    2: Повышение квалификации
    3: Сертификаты
    4: Основное
}
Это информация про образовательные учереждения, которые закончил кандидат.

3. Уровень образования — education_level: {
    1: Среднее
    2: Среднее специальное
    3: Неоконченное высшее
    4: Высшее
    5: Бакалавр
    6: Магистр
    7: Кандидат наук
    8: Доктор наук
}
Это информация про образовательные учереждения, которые закончил кандидат.

3. Уровень знания языка — language_level: {
    1: Начальный
    2: Элементарный
    3: Средний
    4: Средне-продвинутый
    5: Продвинутый
    6: В совершенстве
    7: Родной
}
Иногда кандидаты указывают эту информацию, но не всегда.
```
"""