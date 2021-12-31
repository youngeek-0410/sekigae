from typing import List, Optional, TypeVar
from uuid import UUID

from app.core.exceptions import ApiException, NotFoundObjectMatchingUuid
from sqlalchemy.orm import query, scoped_session

from ..db.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD:
    def __init__(self, db_session: scoped_session, model: ModelType) -> None:
        self.db_session = db_session
        self.model: ModelType = model
        self.model.query = self.db_session.query_property()

    def get_query(self) -> query.Query:
        return self.model.query.filter_by(is_active=True)

    def gets(self, query=None) -> List[ModelType]:
        if query is not None:
            return self.get_query().filter(query).all()
        return self.get_query().all()

    def get_by_uuid(self, uuid: UUID) -> Optional[ModelType]:
        return self.get_query().filter_by(uuid=uuid).first()

    def create(self, data: dict = {}) -> ModelType:
        obj = self.model()
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.add(obj)
        self.db_session.flush()
        self.db_session.refresh(obj)
        return obj

    def update(self, uuid: UUID, data: dict = {}) -> ModelType:
        obj = self.get_by_uuid(uuid)
        if obj is None:
            raise ApiException(NotFoundObjectMatchingUuid(self.model, uuid))
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db_session.flush()
        self.db_session.refresh(obj)
        return obj

    def delete_by_uuid(self, uuid: UUID) -> None:
        obj = self.get_by_uuid(uuid)
        if not obj:
            raise ApiException(NotFoundObjectMatchingUuid(self.model, uuid))
        obj.is_active = False
        self.db_session.flush()
        self.db_session.refresh(obj)
        return None
