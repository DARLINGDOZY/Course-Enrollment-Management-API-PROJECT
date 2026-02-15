from pydantic import BaseModel, ConfigDict

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    role: str

class EnrollmentDelete(EnrollmentBase):
    role: str

class EnrollmentResponse(EnrollmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
