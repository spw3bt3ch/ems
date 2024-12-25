from pydantic import BaseModel
from datetime import datetime
from typing import List


class Department(BaseModel):
    name: str
    head: str


class ShowDept(BaseModel):
    name: str
    head: str

    class Config:
        orm_mode = True


class Employee(BaseModel):
    name: str
    role: str
    department: str

    class Config:
        orm_mode = True


class ShowEmployee(BaseModel):
    name: str
    role: str
    department: str
    dept_info: ShowDept

    class Config:
        orm_mode = True


class EmployeeRM(BaseModel):
    name: str
    role: str
    department: str


class HumanResources(BaseModel):
    fullname: str
    username: str
    password: str

