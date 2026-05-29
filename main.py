from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("students.db", check_same_thread = False)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        course TEXT NOT NULL
    )
''')

conn.commit()

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

@app.get("/")
def home():
    return {"message": "Student management API is running"}

#Create student
@app.put("/student")
def create_student(student: Student):
    cursor.execute("SELECT * FROM Students WHERE id = ?", (student.id,))
    existing_student = cursor.fetchone()

    if existing_student:
        raise HTTPException(
            status_code = 400,
            detail = "Student with this ID already exists"
        )
    
    #Insert student
    cursor.execute(
        "INSERT INTO Students(id, name, age, course) VALUES (?, ?, ?, ?)",
        (student.id, student.name, student.age, student.course)
    )

    conn.commit()

    return {
        "message": "Student created successfully",
        "student": student
    }

#Get all students
@app.get("/student")
def all_students():
    cursor.execute("SELECT * FROM Students")

    students = cursor.fetchall()

    results = []

    for student in students:
        results.append({
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "course": student[3]
        })

    return results


#get single student

@app.get("/student/{student_id}")
def get_student(student_id: int):
    cursor.execute('SELECT * FROM students WHERE id = ?',
                   (student_id,))
    
    student = cursor.fetchone()

    if not student:
        raise HTTPException(
            status_code = 400,
            detail="Student with same id not found"
        )
    
    return {
        "id": student[0],
        "name": student[1],
        "age": student[2],
        "course": student[3]
    }

#update students
@app.put("/students/{student_id}")
def update_students(student_id: int, student: Student):
    cursor.execute("SELECT * FROM Students WHERE id = ?", (student_id,))
    existing_student = cursor.fetchone()

    if not existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student with the given ID not found"
        )
    
    cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?", (student.name,
        student.age,
        student.course,
        student_id))
    conn.commit()

    return {
        "message": "Student updated successfully"
    }

#delete student
@app.put("/student/{student_id}")
def delete_student(student_id: int):
    cursor.execute("SELECT * FROM Students WHERE id=?", (student_id,))
    student = cursor.fetchone()

    if not student:
        raise HTTPException(
            status_code=400,
            detail="Student with the given ID not found"
        )
    
    cursor.execute("DELETE FROM Students WHERE id=?", (student_id,))
    conn.commit()

    return{
        "message": "Student deleted successfully"
    }