from sqlalchemy import Column, String, Integer, TIMESTAMP, text, ForeignKey
from database import Base, engine
from sqlalchemy.orm import relationship


class Employee(Base):
    __tablename__ = "employee_table"

    id = Column(Integer, index=True, primary_key=True)
    dept_id = Column(Integer, ForeignKey("department.id"))
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    # joining_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    dept_info = relationship("Department", back_populates="employee_table")


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String, nullable=False)
    head = Column(String, nullable=False)
    employee_table = relationship("Employee", back_populates="dept_info")


class HumanResources(Base):
    __tablename__ = "admin"

    id = Column(Integer, index=True, primary_key=True)
    fullname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
