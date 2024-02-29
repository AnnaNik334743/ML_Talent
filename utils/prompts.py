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
Do not create any extra fields. Answer in English. Some fields can only have a limited number of values:
```
1.  contact_type: {Phone, Email, Skype, Telegram, Github}
Often contacts are written in the beginning of a CV.

2. education_type: {Elementary, Training, Sertificates, Basic}
This is usually about schools and courses of a candidate.

3. education_level: {Secondary, Secondary professional, Higher incomplete, Higher, Bachelor, Master, PhD, Doctor}
This field is usually about schools and courses of a candidate.

4. language_level: {Beginning, Pre-intermediate, Intermediate, Upper-intermediate, Advanced, Proficient, Native}
Sometimes candidates specify language_level information, but not always, so field can be empty. 
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
Не придумывай лишних полей. Отвечай на русском. Некоторые поля могут иметь только определенные значения:
```
1. Типы контактов — contact_type: {Телефон, Email, Skype, Telegram, Github}
Часто контакты указаны в начале резюме.

2. Виды образования — education_type: {Начальное, Повышение квалификации, Сертификаты, Основное}
Это информация про образование, которое получил кандидат.

3. Уровень образования — education_level: {Среднее, Среднее специальное, Неоконченное высшее, Высшее, Бакалавр, Магистр, Кандидат наук, Доктор наук}
Это информация про образование, которое получил кандидат.

3. Уровень знания языка — language_level: {Начальный, Элементарный, Средний, Средне-продвинутый, Продвинутый, В совершенстве, Родной}
Иногда кандидаты указывают эту информацию, но не всегда, поэтому поле может быть пустым.
```
"""