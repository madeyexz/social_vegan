# main.py
from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException
# from models import Gender, Role, User, UpdateUser
from person_class import Person

app = FastAPI()

