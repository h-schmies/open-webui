import time
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, BigInteger
from open_webui.internal.db import Base, get_db

class Cost(Base):
    __tablename__ = "cost"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    group_id = Column(String, index=True)
    model_id = Column(String, index=True)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    cost = Column(Float)
    created_at = Column(BigInteger, default=lambda: int(time.time()))
    updated_at = Column(BigInteger, default=lambda: int(time.time()))

    def __init__(self, user_id: str, group_id: str, model_id: str, input_tokens: int, output_tokens: int, cost: float):
        self.user_id = user_id
        self.group_id = group_id
        self.model_id = model_id
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cost = cost
        self.created_at = int(time.time())
        self.updated_at = int(time.time())

    def update_cost(self, input_tokens: int, output_tokens: int, cost: float):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cost = cost
        self.updated_at = int(time.time())

    @staticmethod
    def get_cost_by_user_id(user_id: str) -> Optional['Cost']:
        with get_db() as db:
            return db.query(Cost).filter_by(user_id=user_id).first()

    @staticmethod
    def get_cost_by_group_id(group_id: str) -> Optional['Cost']:
        with get_db() as db:
            return db.query(Cost).filter_by(group_id=group_id).first()

    @staticmethod
    def get_cost_by_model_id(model_id: str) -> Optional['Cost']:
        with get_db() as db:
            return db.query(Cost).filter_by(model_id=model_id).first()

    @staticmethod
    def create_cost(user_id: str, group_id: str, model_id: str, input_tokens: int, output_tokens: int, cost: float) -> 'Cost':
        with get_db() as db:
            new_cost = Cost(user_id, group_id, model_id, input_tokens, output_tokens, cost)
            db.add(new_cost)
            db.commit()
            db.refresh(new_cost)
            return new_cost

    @staticmethod
    def update_cost_record(cost_id: str, input_tokens: int, output_tokens: int, cost: float) -> Optional['Cost']:
        with get_db() as db:
            cost_record = db.query(Cost).filter_by(id=cost_id).first()
            if cost_record:
                cost_record.update_cost(input_tokens, output_tokens, cost)
                db.commit()
                db.refresh(cost_record)
                return cost_record
            return None
