from typing import List
from bson import ObjectId
from pymongo import MongoClient
import os
from .models import StudentCreate, StudentUpdate, StudentList, StudentDetail

# Setup MongoDB connection
client = MongoClient(os.getenv("MONGODB_URL"))
db = client.library_management_system  
students_collection = db.students 


def create_student(student_data: StudentCreate) -> dict:
    """Creates a new student document."""
    student = student_data.dict(by_alias=True)  
    result = students_collection.insert_one(student)
    return {"id": str(result.inserted_id)}


def get_students(filters: dict = {}) -> List[StudentList]:
    students = []
    for student_document in students_collection.find(filters):
        student_document["_id"] = str(student_document["_id"])
        student = StudentList(**student_document)
        students.append(student)
    return students


def get_student_by_id(student_id: str) -> StudentDetail:
    student_document = students_collection.find_one({"_id": ObjectId(student_id)})
    print(student_document)
    if student_document:
        return StudentDetail(**student_document)
    else:
        return None



def update_student(student_id: str, student_data: StudentUpdate) -> bool:
    updated_data = student_data.dict(exclude_unset=True)
    update_dict = {}
    for key, value in updated_data.items():
        if isinstance(value, dict):  
            for sub_key, sub_value in value.items():
                update_dict[f"{key}.{sub_key}"] = sub_value
        else:
            update_dict[key] = value
    print("hello " )
    print(update_dict)
    result = students_collection.update_one(
        {"_id": ObjectId(student_id)}, {"$set": update_dict}
    )
    return result.modified_count > 0

def delete_student(student_id: str) -> bool:
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0

