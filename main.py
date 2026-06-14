from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Student
from schemas import StudentSchema
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def status() -> dict:
    return {"status": "ok", "message": "Welcome to FastAPI"}

@app.get("/Students", response_model=list[StudentSchema])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/Students/{id}", response_model=StudentSchema)
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/Students", response_model=StudentSchema)
def create_student(student: StudentSchema, db: Session = Depends(get_db)):
    logger.info(f"Registering new student: {student.name} ({student.email})")
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    logger.info(f"Student registered successfully with ID: {db_student.id}")
    return db_student

@app.put("/Students/{id}", response_model=StudentSchema)
def update_student(id: int, student: StudentSchema, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/Students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}
