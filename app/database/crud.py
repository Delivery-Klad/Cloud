from sqlalchemy.orm import Session

from app.database import schemas, models


def set_default_parameters(db: Session):
    db_data = db.query(models.Controller).first()
    if db_data is None:
        data = models.Controller(enable=0)
        db.add(data)
        db.commit()


def get_controller(db: Session):
    db_data = db.query(models.Controller).first()
    return db_data.enable
