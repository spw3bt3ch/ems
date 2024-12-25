from fastapi import FastAPI, Depends, status
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import schemas
from schemas import Employee
import model
from typing import List

# Employee Management System

# Features:
# CRUD Operations: Add, update, delete, and retrieve employee details.
# Authentication: Admin login for managing employees.
# Search and Filters: Query employees by role, department, or joining date.
# Database: Use SQLAlchemy to model employees, departments, and attendance data.
# Use Case: HR teams can use it to manage and track employee records efficiently.

# Operations/HTTP Methods: POST, GET (Retrieve all, by role, by department, joining date),  PUT, DELETE
# Tables Fields: id, Name, Role, Department, Joining date

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="HR teams can use it to manage and track employee records efficiently",
    version="0.1.2"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/employee', tags=['Employees'], response_model=List[schemas.ShowEmployee])
async def all_employees(db: Session = Depends(get_db)):
    employees = db.query(model.Employee).all()
    if employees:
        return employees
    else:
        return {'Message': 'Employee List is presently empty'}


@app.post('/employee', tags=['Employees'])
async def create_employee(request: schemas.Employee, db: Session = Depends(get_db)):
    create = model.Employee(name=request.name, role=request.role, department=request.department, dept_id=1)
    db.add(create)
    db.commit()
    db.refresh(create)
    return {'Message': 'An employee record has been created'}


@app.delete('/employee', status_code=status.HTTP_200_OK, tags=['Employees'])
async def remove_employee(employee_id, db: Session = Depends(get_db)):
    employee_to_remove = db.query(model.Employee).filter(model.Employee.id == employee_id).first()
    if employee_to_remove:
        db.delete(employee_to_remove)
        db.commit()
        return f'An employee with the ID of {employee_id} has been removed.'
    else:
        return f'Can\'t perform operation because employee ID does not exist!'


@app.put('/employee', tags=['Employees'])
async def update_employee_record(id, request: schemas.Employee, db: Session = Depends(get_db)):
    db.query(model.Employee).filter(model.Employee.id == id).update(
        {'name': request.name, 'role': request.role, 'department': request.department})
    db.commit()
    return f'Employee with the ID of {id} has been updated.'


@app.get('/employee/{role}', tags=['Employees'])
async def get_employees_by_role(role: str, db: Session = Depends(get_db)):
    employee_role = db.query(model.Employee).filter(model.Employee.role == role).all()
    if employee_role:
        return employee_role
    else:
        return 'This role does not exit in the database'


@app.get('/employee_dept/{department}', tags=['Employees'])
async def get_employees_by_dept(department: str, db: Session = Depends(get_db)):
    employee_dept = db.query(model.Employee).filter(model.Employee.department == department).all()
    if employee_dept:
        return employee_dept
    else:
        return 'Department does not exit in the database'


@app.get('/employee_id/{id}', tags=['Employees'])
async def get_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(model.Employee).filter(model.Employee.id == id).first()
    if employee:
        return employee
    else:
        return f'Employee with the ID {id} does not exit in the database'


@app.post('/Department', tags=['Departments'])
async def create_department(request: schemas.Department, db: Session = Depends(get_db)):
    dept = model.Department(name=request.name, head=request.head)
    db.add(dept)
    db.commit()
    return 'A Department has been created successfully'


@app.get('/Department', tags=['Departments'])
async def get_all_dept(db: Session = Depends(get_db)):
    all_dept = db.query(model.Department).all()
    if all_dept:
        return all_dept
    else:
        return 'Department List is Empty'


@app.put('/Department', tags=['Departments'])
async def update_department(dept_id, request: schemas.Department, db: Session = Depends(get_db)):
    dept_update = db.query(model.Department).filter(model.Department.id == dept_id).update(
        {'name': request.name, 'head': request.head})
    db.commit()
    if dept_update:
        return f'The department with an ID of {dept_id} has been updated successfully'
    else:
        return 'Department does not exist'


@app.delete('/Department/{dept_id}', tags=['Departments'])
async def remove_dept(dept_id, db: Session = Depends(get_db)):
    dept_to_remove = db.query(model.Department).filter(model.Department.id == dept_id).first()
    if dept_to_remove:
        db.delete(dept_to_remove)
        db.commit()
        return f'The department with an Id of {dept_id} has been removed successfully'
    else:
        return 'This department is not available to be removed'


@app.post('/hr', tags=['Human Resources'])
async def human_resources(request: schemas.HumanResources, db: Session = Depends(get_db)):
    new_admin = model.HumanResources(fullname=request.fullname, username=request.username, password=request.password)
    db.add(new_admin)
    db.commit()
    return {'A new admin has been added successfully'}


@app.get('/hr', tags=['Human Resources'])
async def view_all_admin(db: Session = Depends(get_db)):
    get_admin = db.query(model.HumanResources).all()
    if get_admin:
        return get_admin
    else:
        return 'Admin does not exist'


@app.put('/hr', tags=['Human Resources'])
async def update_admin(id, request: schemas.HumanResources, db: Session = Depends(get_db)):
    admin = db.query(model.HumanResources).filter(model.HumanResources.id == id).update(
        {'fullname': request.fullname, 'username': request.username, 'password': request.password}
    )
    if admin:
        db.commit()
        return f'Admin with the ID of {id} has been updated successfully'
    else:
        return f'Admin ID {id} does not exist'


@app.delete('/hr', tags=['Human Resources'])
async def remove_admin(id, db: Session = Depends(get_db)):
    delete_admin = db.query(model.HumanResources).filter(model.HumanResources.id == id).first()
    if delete_admin:
        db.delete(delete_admin)
        db.commit()
        return 'An Admin has just been removed from the database'
    else:
        return f'Admin with the ID of {id} is not in the database'


# Admin Login to access Employees data
# @app.patch('/hr', tags=['Human Resources'])
# async def login(id, request: schemas.HumanResources, db: Session = Depends(get_db)):
#     pass
