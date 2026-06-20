from pydantic import BaseModel

class StudentSchema(BaseModel):
    id: int
    name: str
    email: str
    mobile: str
    place: str

    class Config:
        from_attributes = True
