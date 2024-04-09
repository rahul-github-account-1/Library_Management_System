from typing import Optional
from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    country: str

class StudentBase(BaseModel):
    name: str
    age: int


class StudentList(BaseModel):
    name: str
    age: int

class StudentDetail(StudentBase):
    address: Address

class StudentCreate(StudentBase):
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

class StudentInDBBase(StudentBase):
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class Student(StudentInDBBase):

    address: Address

class StudentInDB(StudentInDBBase):
    pass
