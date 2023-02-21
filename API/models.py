from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Date, JSON
from sqlalchemy.orm import relationship
from database import Base

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_name = Column(String)
    default = Column(Boolean, default=False, index=True) 
    permissions = Column(Integer)

    users = relationship("Users", back_populates="roles")



class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    cpf = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String)
    email = Column(String, nullable=False, index=True)
    hash_password = Column(String, nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    creation_at = Column(DateTime)
    status = Column(Boolean)
    last_email_modified = Column(DateTime)
    last_password_modified = Column(DateTime)
    last_activity = Column(DateTime)
    last_payment = Column(DateTime)