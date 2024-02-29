import uvicorn
import tempfile
from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from parsing import *
from json_schemas import Resume
from openai import OpenAI
from prompts import ENGLISH_PROMPT, RUSSIAN_PROMPT
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv('API_KEY')
GPT_MODEL = os.getenv('GPT_MODEL')
CLIENT = OpenAI(api_key=API_KEY)
MODEL = YOLO('yolov8s.pt')

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
    global MODEL

    # Get file extension
    file_extension = get_filename_extension(file.filename)

    # Create a temporary file and save the uploaded file to it
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(file.file, temp_file)
    file_path = temp_file.name

    # Parse the file
    data = parse(file_path, file_extension, MODEL)

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
    global GPT_MODEL, RUSSIAN_PROMPT, ENGLISH_PROMPT

    if prompt_language == 'ru':
        d = {"messages": [{"role": "system", "content": f"{RUSSIAN_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}
    else:
        d = {"messages": [{"role": "system", "content": f"{ENGLISH_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}

    # response = CLIENT.chat.completions.create(
    #     model=GPT_MODEL,
    #     messages=d['messages']
    # )
    #
    # content = response.choices[0].message.content

    content = "{'resume': {'resume_id': '', 'first_name': 'Антон', 'last_name': 'Бармин', 'middle_name': 'Сергеевич', 'birth_date': '1995-06-14', 'birth_date_year_only': 'false', 'country': 'Россия', 'city': 'Белгород', 'about': 'Experienced Python developer with a focus on ML, DL, Computer Vision, and System Design. Currently exploring mathematics and mathematical modeling.', 'key_skills': ['Python', 'SQL', 'R', 'FastAPI', 'Flask', 'Pytest', 'Postgres', 'Airflow', 'Torch', 'Tensorflow', 'sklearn', 'xgboost', 'pandas', 'numpy', 'statsmodels', 'ggplot2', 'caret', 'Redis', 'GIT', 'Jira', 'Docker', 'Triton-Inference-Server'], 'salary_expectations_amount': '', 'salary_expectations_currency': '', 'photo_path': '', 'language': 'ru', 'gender': 'male', 'resume_name': '', 'source_link': '', 'contactItems': [{'resume_contact_item_id': '', 'value': '89190008691', 'comment': '', 'contact_type': 'Phone'}, {'resume_contact_item_id': '', 'value': 'barmiaa43@mail.ru', 'comment': '', 'contact_type': 'Email'}], 'educationItems': [{'resume_education_item_id': '', 'year': 2017, 'organization': 'БГТУ им. В.Г.Шухова', 'faculty': 'Кафедра “Технической кибернетики”', 'specialty': 'мехатроника и робототехника', 'result': '', 'education_type': 'Basic', 'education_level': 'Bachelor'}, {'resume_education_item_id': '', 'year': 2019, 'organization': 'БГТУ им. В.Г.Шухова', 'faculty': 'Кафедра “Программное обеспечение вычислительной техники и автоматизированных систем', 'specialty': 'информатика и вычислительная техника', 'result': '', 'education_type': 'Basic', 'education_level': 'Bachelor'}], 'experienceItems': [{'resume_experience_item_id': '', 'starts': 2020, 'ends': '', 'employer': 'ООО “Наполеон АЙТИ', 'city': '', 'url': '', 'position': 'Senior Python Developer', 'description': 'ML System Design, Backend development, Model training and deployment.', 'order': 3}, {'resume_experience_item_id': '', 'starts': 2022, 'ends': 2024, 'employer': 'AI Talent Hub', 'city': '', 'url': '', 'position': 'Mentor', 'description': 'Mentoring students on Deep Learning course.', 'order': 2}, {'resume_experience_item_id': '', 'starts': 2018, 'ends': 2020, 'employer': 'ООО “Фабрика информационных технологий”', 'city': '', 'url': '', 'position': 'Python Developer', 'description': 'ML System Design, Backend development, Model training and deployment. Achievements: Recognized for excellence in license plate recognition services.', 'order': 1}], 'languageItems': [{'resume_language_item_id': '', 'language': 'English', 'language_level': 'Intermediate'}]}}"
    # content = eval(content.replace('\"', '\\"').replace('\"\'', '\\"\"').replace('\'\"', '\'\\"').replace("\'", '\"'))

    return eval(content)


@app.post("/parse_file", response_model=Resume)
async def parse_file(file: UploadFile = File(...)):
    """
    Parses a file uploaded via the API and returns a Resume object containing the extracted information.

    Parameters:
        file (UploadFile): The uploaded file containing the document.

    Returns:
        Resume: The parsed resume object.
    """
    data = await extract_text(file)
    result = await parse_text_with_llm(data.text, data.language)

    result['resume']['photo_path'] = data.photo_path

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
