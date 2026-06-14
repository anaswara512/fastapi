from pydantic import BaseModel

class StudentSchema(BaseModel):
    id: int
    name: str
    email: str
    mobile: int
    place: str

    class Config:
        from_attributes = True
