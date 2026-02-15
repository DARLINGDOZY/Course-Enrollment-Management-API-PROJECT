from pydantic import BaseModel, Field, ConfigDict

class CourseBase(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: str = Field(None, min_length=1)
    code: str = Field(None, min_length=1)

class CourseResponse(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
