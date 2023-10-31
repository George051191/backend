import pydantic


class UniversityDTO(pydantic.BaseModel):
    name: str