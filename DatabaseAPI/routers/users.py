from fastapi import status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
import models, schemas
from database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def new_user(new_user: schemas.UserBase, db: Session = Depends(get_db)) -> schemas.User:
    try:
        user_data = models.User(**new_user.dict())
        try:
            db.add(user_data)
            db.commit()
            db.refresh(user_data)
            return user_data
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="CPF ou e-mail já cadastrados!")
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Json inválido!")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.User])
async def get_all_users(db: Session = Depends(get_db)) -> list[schemas.User]:
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def update_user(user_id: int, updated_user: schemas.User, db: Session = Depends(get_db)) -> schemas.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db.query(models.User).filter(models.User.id == user_id).update(updated_user.dict())
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
