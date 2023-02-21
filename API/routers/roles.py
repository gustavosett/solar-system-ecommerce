from fastapi import status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
import models, schemas
from database import get_db


router = APIRouter(
    prefix = "/roles",
    tags = ["roles"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RoleBase)
async def new_role(new_role: schemas.RoleBase, db: Session = Depends(get_db)) -> schemas.RoleBase:
    print(db)
    print(new_role)
    print(db.query(models.Role).all())
    try:
        role_data = models.Role(**new_role.dict())
        try:
            db.add(role_data)
            db.commit()
            db.refresh(role_data)
            return role_data
        except:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= f"Desculpe, essa role não está disponível!")
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"Json inválido!")
