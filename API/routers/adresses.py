from fastapi import status, Depends, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Address)
async def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)) -> schemas.Address:
    try:
        db_address = models.Address(**address.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        # definindo todos os endereços para secundário caso seja um endereço primário.
        if db_address.is_primary:
            (db.query(models.Address)
                .filter(
                    models.Address.id != db_address.id,
                    models.Address.user_id == db_address.user_id,
                    models.Address.is_primary == True
                )
                .update(
                    {models.Address.is_primary: False}
                )
            )
            db.commit()
        return db_address
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Address already exists")


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Address])
async def read_addresses(db: Session = Depends(get_db)) -> List[schemas.Address]:
    return db.query(models.Address).all()


@router.get("/{address_id}", status_code=status.HTTP_200_OK, response_model=schemas.Address)
async def read_address(address_id: int, db: Session = Depends(get_db)) -> schemas.Address:
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return db_address


@router.put("/{address_id}", status_code=status.HTTP_200_OK, response_model=schemas.Address)
async def update_address(address_id: int, address: schemas.Address, db: Session = Depends(get_db)) -> schemas.Address:
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    for var, value in address:
        setattr(db_address, var, value)
    db.commit()
    db.refresh(db_address)
    # definindo todos os endereços para secundário caso seja um endereço primário.
    if db_address.is_primary:
        (db.query(models.Address)
            .filter(
                models.Address.id != db_address.id,
                models.Address.user_id == db_address.user_id,
                models.Address.is_primary == True
            )
            .update(
                {models.Address.is_primary: False}
            )
        )
        db.commit()
    return db_address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    next_address = (
        db.query(models.Address)
        .filter(
            models.Address.user_id == db_address.user_id,
            models.Address.id != db_address.id
        )
        .order_by(models.Address.id.asc())
        .first()
    )
    if next_address:
        next_address.is_primary = True

    db.delete(db_address)
    db.commit()

