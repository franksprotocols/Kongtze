"""Rewards and gamification routes for Kongtze API"""

import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.models.reward import Reward
from app.models.gift import Gift
from app.models.user import User
from app.schemas.reward import (
    RewardResponse,
    GiftResponse,
    GiftCreate,
    LuckyDrawResult,
)
from app.api.deps import get_current_user, get_current_parent

router = APIRouter(prefix="/rewards", tags=["Rewards & Gamification"])


@router.get("/balance", response_model=dict)
async def get_reward_balance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get the current user's reward points balance.

    Returns the current balance and total points earned.
    """
    # Get latest reward transaction for balance
    result = await db.execute(
        select(Reward)
        .where(Reward.user_id == current_user.user_id)
        .order_by(Reward.created_at.desc())
        .limit(1)
    )
    latest_reward = result.scalar_one_or_none()

    if not latest_reward:
        return {"balance": 0, "total_earned": 0}

    # Calculate total earned (sum of positive points)
    result = await db.execute(
        select(Reward)
        .where(and_(
            Reward.user_id == current_user.user_id,
            Reward.points > 0,
        ))
    )
    all_rewards = result.scalars().all()
    total_earned = sum(r.points for r in all_rewards)

    return {
        "balance": latest_reward.balance,
        "total_earned": total_earned,
    }


@router.get("/history", response_model=List[RewardResponse])
async def get_reward_history(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[RewardResponse]:
    """
    Get reward transaction history for the current user.

    - **limit**: Maximum number of transactions to return (default: 50)
    """
    result = await db.execute(
        select(Reward)
        .where(Reward.user_id == current_user.user_id)
        .order_by(Reward.created_at.desc())
        .limit(limit)
    )
    rewards = result.scalars().all()

    return [RewardResponse.model_validate(r) for r in rewards]


# Gift management routes (parent only)


@router.post("/gifts", response_model=GiftResponse, status_code=status.HTTP_201_CREATED)
async def create_gift(
    gift_data: GiftCreate,
    db: AsyncSession = Depends(get_db),
    current_parent: User = Depends(get_current_parent),
) -> GiftResponse:
    """
    Create a new gift for the lucky draw catalog (parent only).

    - **name**: Gift name
    - **description**: Gift description
    - **tier**: Tier (gold/silver/bronze)
    - **probability**: Probability of winning (0.0-1.0)
    - **image_path**: Optional image path
    """
    new_gift = Gift(
        name=gift_data.name,
        description=gift_data.description,
        tier=gift_data.tier,
        probability=gift_data.probability,
        image_path=gift_data.image_path,
    )

    db.add(new_gift)
    await db.flush()
    await db.refresh(new_gift)

    return GiftResponse.model_validate(new_gift)


@router.get("/gifts", response_model=List[GiftResponse])
async def get_gifts(
    tier: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[GiftResponse]:
    """
    Get all available gifts in the lucky draw catalog.

    - **tier**: Optional filter by tier (gold/silver/bronze)
    """
    query = select(Gift)

    if tier:
        query = query.where(Gift.tier == tier)

    query = query.order_by(Gift.probability.desc())

    result = await db.execute(query)
    gifts = result.scalars().all()

    return [GiftResponse.model_validate(g) for g in gifts]


@router.delete("/gifts/{gift_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gift(
    gift_id: int,
    db: AsyncSession = Depends(get_db),
    current_parent: User = Depends(get_current_parent),
) -> None:
    """
    Delete a gift from the catalog (parent only).

    - **gift_id**: The gift ID
    """
    result = await db.execute(
        select(Gift).where(Gift.gift_id == gift_id)
    )
    gift = result.scalar_one_or_none()

    if not gift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found",
        )

    await db.delete(gift)


# Lucky draw functionality


@router.post("/lucky-draw", response_model=LuckyDrawResult)
async def lucky_draw(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LuckyDrawResult:
    """
    Perform a lucky draw (costs 100 points).

    Randomly selects a gift based on probability weights.
    Deducts 100 points from user's balance.
    """
    LUCKY_DRAW_COST = 100

    # Get current balance
    result = await db.execute(
        select(Reward)
        .where(Reward.user_id == current_user.user_id)
        .order_by(Reward.created_at.desc())
        .limit(1)
    )
    latest_reward = result.scalar_one_or_none()
    current_balance = latest_reward.balance if latest_reward else 0

    # Check if user has enough points
    if current_balance < LUCKY_DRAW_COST:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient points. You need {LUCKY_DRAW_COST} points (current: {current_balance})",
        )

    # Get all available gifts
    result = await db.execute(select(Gift))
    gifts = result.scalars().all()

    if not gifts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No gifts available in the lucky draw catalog",
        )

    # Select gift based on probability weights
    weights = [gift.probability for gift in gifts]
    selected_gift = random.choices(gifts, weights=weights, k=1)[0]

    # Deduct points
    new_balance = current_balance - LUCKY_DRAW_COST

    reward = Reward(
        user_id=current_user.user_id,
        points=-LUCKY_DRAW_COST,
        reason=f"Lucky draw - won {selected_gift.name}",
        balance=new_balance,
    )

    db.add(reward)
    await db.flush()

    return LuckyDrawResult(
        gift=GiftResponse.model_validate(selected_gift),
        points_spent=LUCKY_DRAW_COST,
        remaining_balance=new_balance,
    )
