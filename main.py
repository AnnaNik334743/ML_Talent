import shutil
import uvicorn
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from parsing_utils import parse
from json_schemas import Resume, ParserOutput
from config import OPENAI_CLIENT, OPENAI_MODEL_NAME
from prompts import ENGLISH_PROMPT, RUSSIAN_PROMPT
from utils import postprocess_special_fields


app = FastAPI()


def get_filename_extension(filename: str) -> str:
    """
    Extracts the file extension from a filename.

    Parameters:
        filename (str): The name of the file.

    Returns:
        str: The file extension.
    """
    return filename.split('.')[-1]


@app.post("/extract_text", response_model=ParserOutput)
async def extract_text(file: UploadFile = File(...)):
    """
   Extracts text from an uploaded file.

   Parameters:
       file (UploadFile): The uploaded file containing the document.

   Returns:
       ParserOutput: The parsed output containing extracted text and metadata.
    """
    # Get file extension
    file_extension = get_filename_extension(file.filename)

    # Create a temporary file and save the uploaded file to it
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(file.file, temp_file)
    file_path = temp_file.name

    # Parse the file
    data = parse(file_path, file_extension)

    # Close and remove the temporary file
    temp_file.close()

    return data


@app.post("/parse_text", response_model=Resume)
async def parse_text_with_llm(text: str, prompt_language: str):
    """
    Parses text using a language model and returns a Resume object containing the extracted information.

    Parameters:
        text (str): The text of resume to be parsed.
        prompt_language (str): The language of the text prompt ('ru' for Russian, 'en' for English).

    Returns:
        Resume: The parsed resume object.
    """
    if prompt_language == 'ru':
        d = {"messages": [{"role": "system", "content": f"{RUSSIAN_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}
    else:
        d = {"messages": [{"role": "system", "content": f"{ENGLISH_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}

    # response = OPENAI_CLIENT.chat.completions.create(
    #     model=OPENAI_MODEL_NAME,
    #     messages=d['messages']
    # )
    #
    # content = response.choices[0].message.content

    content = """{
  "resume": {
    "resume_id": "",
    "first_name": "Антон",
    "last_name": "Бармин",
    "middle_name": "Сергеевич",
    "birth_date": "1995-06-14",
    "birth_date_year_only": False,
    "country": "Россия",
    "city": "Белгород",
    "about": "С 2018 года занимаюсь разработкой на Python, основные сферы деятельности: ML, DL, Computer Vision, System Design. Текущее направление развития – математика, математическое моделирование.",
    "key_skills": [
      "Python",
      "SQL",
      "R",
      "FastAPI",
      "Flask",
      "Pytest",
      "Postgres",
      "Airflow",
      "Torch",
      "Tensorflow",
      "sklearn",
      "xgboost",
      "pandas",
      "numpy",
      "statsmodels",
      "ggplot2",
      "caret",
      "Redis",
      "GIT",
      "Jira",
      "Docker",
      "Docker-compose",
      "Triton-Inference-Server"
    ],
    "salary_expectations_amount": "",
    "salary_expectations_currency": "",
    "photo_path": "",
    "language": "ru",
    "gender": "муж",
    "resume_name": "",
    "source_link": "",
    "contactItems": [
      {
        "resume_contact_item_id": "",
        "value": "89190008691",
        "comment": "",
        "contact_type": "Телефон"
      },
      {
        "resume_contact_item_id": "",
        "value": "barmiaa43@mail.ru",
        "comment": "",
        "contact_type": "Email"
      }
    ],
    "educationItems": [
      {
        "resume_education_item_id": "",
        "year": 2017,
        "organization": "БГТУ им. В.Г.Шухова",
        "faculty": "Кафедра “Технической кибернетики”",
        "specialty": "мехатроника и робототехника",
        "result": "",
        "education_type": "Основное",
        "education_level": "Бакалавр"
      },
      {
        "resume_education_item_id": "",
        "year": 2019,
        "organization": "БГТУ им. В.Г.Шухова",
        "faculty": "Кафедра “Программное обеспечение вычислительной техники и автоматизированных систем”",
        "specialty": "информатика и вычислительная техника",
        "result": "",
        "education_type": "Основное",
        "education_level": "Магистр"
      }
    ],
    "experienceItems": [
      {
        "resume_experience_item_id": "",
        "starts": 2020,
        "ends": "",
        "employer": "ООО “Наполеон АЙТИ”",
        "city": "",
        "url": "",
        "position": "Senior Python Developer",
        "description": "Backend разработка; ML System Design; Обучение, деплой моделей. Projects: Распознавание запрещенного контента, “Гранулометрия”, “Антифрод”, Доработка внутренних ML сервисов компании.",
        "order": 3
      },
      {
        "resume_experience_item_id": "",
        "starts": 2022,
        "ends": 2024,
        "employer": "AI Talent Hub",
        "city": "",
        "url": "",
        "position": "Mentor",
        "description": "Менторство студентов на курсе “Глубокое обучение на практике”",
        "order": 2
      },
      {
        "resume_experience_item_id": "",
        "starts": 2018,
        "ends": 2020,
        "employer": "ООО “Фабрика информационных технологий”",
        "city": "",
        "url": "",
        "position": "Python Developer",
        "description": "Backend разработка; ML System Design; Обучение, деплой моделей. Projects: Распознавание автомобильных номеров (v1), Сервис внутренней аналитики, Распознавание автомобильных номеров (v2). Achievements: один из лучших на рынке сервисов по распознаванию номеров на момент 2020г. (согласно внутреннему исследованию компании).",
        "order": 1
      }
    ],
    "languageItems": [
      {
        "resume_language_item_id": "",
        "language": "Английский",
        "language_level": "Средний"
      }
    ]
  }
}"""

    return eval(content)


def prettify_output(d: 'Resume') -> dict:
    return postprocess_special_fields(d)


@app.post("/parse_file", response_model=Resume)
async def parse_file(file: UploadFile = File(...), prettify_result: bool = False):
    """
    Parses a file uploaded via the API and returns a Resume object containing the extracted information.

    Parameters:
        file (UploadFile): The uploaded file containing the document.
        prettify_result: Output contains number mappers (contact_type, education_type, etc.) if set to false, 
        otherwise human-readable mapping

    Returns:
        Resume: The parsed resume object.
    """
    data = await extract_text(file)
    result = await parse_text_with_llm(data.text, data.language)

    result['resume']['photo_path'] = data.photo_path

    return result if prettify_result else postprocess_special_fields(result)


# @app.get("/download_file")
# async def download_file(local_file_path: str):
#     """
#     Returns a locally stored file to the user via API.
#     The file_path can be taken from JSON returned by the parse_file or parse_text method.
#     """
#     return FileResponse(local_file_path, media_type='application/octet-stream', filename='file.jpg')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
