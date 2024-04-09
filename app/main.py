from fastapi import FastAPI, HTTPException, Body, Path, status , Response
from typing import List, Optional
from . import crud, models

app = FastAPI(title="Library Management System", version="1.0.0")

@app.post("/students",  status_code=status.HTTP_201_CREATED)
async def create_student(student: models.StudentCreate):
    new_student_id = crud.create_student(student)
    return new_student_id

@app.get("/students", response_model=List[models.StudentList])
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    filters = {}
    if country:
        filters["address.country"] = country
    if age is not None:
        filters["age"] = {"$gte": age}
    students = crud.get_students(filters)
    return students



@app.get("/students/{id}", response_model=models.StudentDetail)
async def fetch_student(id: str = Path(..., title="The ID of the student to get")):
    student = crud.get_student_by_id(id)
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")

@app.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id: str = Path(..., title="The ID of the student to update"),
                         student_data: models.StudentUpdate = Body(...)):
    successful_update = crud.update_student(id, student_data)
    if successful_update:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")


@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student(id: str = Path(..., title="The ID of the student to delete")):
    if crud.delete_student(id):
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
