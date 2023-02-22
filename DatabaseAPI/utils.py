from json import dumps, loads
from sqlalchemy.orm.session import Session
from schemas import *
from models import *

def serializer(obj):
        try:
            cache = dumps(str(obj))
        except:
            cache = {"error": "invalid serialization"}
        return loads(cache)


def exists_by_id(db: Session, Class, Object_id: int) -> bool:
    try:
        query = db.query(Class).filter(Class.id == Object_id).first()
        if query:
            return True
        else:
            return False
    except:
        return False