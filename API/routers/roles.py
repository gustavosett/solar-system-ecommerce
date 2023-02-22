from fastapi import status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
import models, schemas
from database import get_db


router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Role)
async def new_role(new_role: schemas.RoleBase, db: Session = Depends(get_db)) -> schemas.Role:
    try:
        role_data = models.Role(**new_role.dict())
        try:
            db.add(role_data)
            db.commit()
            db.refresh(role_data)
            return role_data
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Desculpe, essa role não está disponível!")
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Json inválido!")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Role])
async def get_all_roles(db: Session = Depends(get_db)) -> list[schemas.Role]:
    roles = db.query(models.Role).all()
    return roles


@router.get("/{role_id}", status_code=status.HTTP_200_OK, response_model=schemas.Role)
async def get_role_by_id(role_id: int, db: Session = Depends(get_db)) -> schemas.Role:
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role não encontrada")
    return role


@router.put("/{role_id}", status_code=status.HTTP_200_OK, response_model=schemas.Role)
async def update_role(role_id: int, updated_role: schemas.RoleBase, db: Session = Depends(get_db)) -> schemas.Role:
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role não encontrada")
    db.query(models.Role).filter(models.Role.id == role_id).update(updated_role.dict())
    db.commit()
    db.refresh(role)
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role não encontrada")
    db.delete(role)
    db.commit()
