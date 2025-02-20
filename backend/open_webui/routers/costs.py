from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from open_webui.internal.db import get_db
from open_webui.models.costs import Cost
from open_webui.utils.auth import get_admin_user, get_verified_user

router = APIRouter()

@router.get("/costs/user/{user_id}", response_model=List[Cost])
async def get_costs_by_user_id(user_id: str, db: Session = Depends(get_db), user=Depends(get_verified_user)):
    costs = db.query(Cost).filter(Cost.user_id == user_id).all()
    if not costs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Costs not found for the given user ID")
    return costs

@router.get("/costs/group/{group_id}", response_model=List[Cost])
async def get_costs_by_group_id(group_id: str, db: Session = Depends(get_db), user=Depends(get_verified_user)):
    costs = db.query(Cost).filter(Cost.group_id == group_id).all()
    if not costs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Costs not found for the given group ID")
    return costs

@router.get("/costs/model/{model_id}", response_model=List[Cost])
async def get_costs_by_model_id(model_id: str, db: Session = Depends(get_db), user=Depends(get_verified_user)):
    costs = db.query(Cost).filter(Cost.model_id == model_id).all()
    if not costs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Costs not found for the given model ID")
    return costs

@router.post("/costs", response_model=Cost)
async def create_cost(cost: Cost, db: Session = Depends(get_db), user=Depends(get_admin_user)):
    db.add(cost)
    db.commit()
    db.refresh(cost)
    return cost

@router.put("/costs/{cost_id}", response_model=Cost)
async def update_cost(cost_id: str, cost: Cost, db: Session = Depends(get_db), user=Depends(get_admin_user)):
    cost_record = db.query(Cost).filter(Cost.id == cost_id).first()
    if not cost_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost record not found")
    cost_record.update_cost(cost.input_tokens, cost.output_tokens, cost.cost)
    db.commit()
    db.refresh(cost_record)
    return cost_record
