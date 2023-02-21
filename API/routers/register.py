from fastapi import status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
import schemas, models
from database import get_db


router = APIRouter(
    prefix = "/register",
    tags = ["register"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
async def register(new_user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserCreate:
    try:
        if new_user.password == new_user.confirm_password:
            new_user_data = schemas.UserBase(new_user)
            print("erro aqui.")
            user_data = models.User(**new_user_data.dict())
            db.add(user_data)
            db.commit()
            db.refresh(user_data)
            return user_data
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"Desculpe, esse usuário não está disponível!")