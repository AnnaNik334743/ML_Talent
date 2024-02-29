from typing import List
from pydantic import BaseModel
import re


def simple_postprocessing(text):
    return re.sub(r'\n{3,}', '\n\n', text).strip()


class TruncParserOutput(BaseModel):
    photo_path: str = ""
    text: str = ""


class ParserOutput(BaseModel):
    photo_path: str = ""
    text: str = ""
    file_extension: str = ""
    language: str = ""

    @classmethod
    def create_from_text(cls, text: str) -> 'ParserOutput':
        """
        Create a ParserOutput object from text input with preprocessing.
        """
        preprocessed_text = simple_postprocessing(text)
        return cls(text=preprocessed_text)


class ContactItem(BaseModel):
    resume_contact_item_id: str | int = ""
    value: str = ""
    comment: str = ""
    contact_type: str = ""


class EducationItem(BaseModel):
    resume_education_item_id: str | int = ""
    year: str | int = ""
    organization: str = ""
    faculty: str = ""
    specialty: str = ""
    result: str = ""
    education_type: str = ""
    education_level: str = ""


class ExperienceItem(BaseModel):
    resume_experience_item_id: str | int = ""
    starts: str | int = ""
    ends: str | int = ""
    employer: str = ""
    city: str = ""
    url: str = ""
    position: str = ""
    description: str = ""
    order: str | int = ""


class LanguageItem(BaseModel):
    resume_language_item_id: str | int = ""
    language: str = ""
    language_level: str | int = ""


class ResumeInner(BaseModel):
    resume_id: str | int = ""
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    birth_date: str = ""
    birth_date_year_only: bool = False
    country: str = ""
    city: str = ""
    about: str = ""
    key_skills: str | list[str] = ""
    salary_expectations_amount: str = ""
    salary_expectations_currency: str = ""
    photo_path: str = ""
    language: str = ""
    gender: str = ""
    resume_name: str = ""
    source_link: str = ""
    contactItems: List[ContactItem] = []
    educationItems: List[EducationItem] = []
    experienceItems: List[ExperienceItem] = []
    languageItems: List[LanguageItem] = []


class Resume(BaseModel):
    resume: ResumeInner
