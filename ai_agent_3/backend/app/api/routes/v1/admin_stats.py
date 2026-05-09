"""Admin overview stats — single endpoint that powers the /admin landing page."""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter
from sqlalchemy import func, select

from app.api.deps import CurrentAppAdmin, DBSession
from app.db.models.conversation import Conversation, Message
from app.db.models.session import Session
from app.db.models.user import User

router = APIRouter()


@router.get("")
async def admin_stats(_: CurrentAppAdmin, db: DBSession) -> dict[str, Any]:
    """Workspace-wide counts + last-24h activity. Cheap aggregates only."""
    now = datetime.now(UTC)
    last_24h = now - timedelta(hours=24)
    last_30d = now - timedelta(days=30)

    total_users = (await db.execute(select(func.count()).select_from(User))).scalar_one()
    total_conversations = (
        await db.execute(select(func.count()).select_from(Conversation))
    ).scalar_one()
    total_messages = (await db.execute(select(func.count()).select_from(Message))).scalar_one()

    active_users_24h = (
        await db.execute(
            select(func.count(func.distinct(Session.user_id))).where(
                Session.last_used_at >= last_24h
            )
        )
    ).scalar_one()

    return {
        "total_users": total_users,
        "active_users_24h": active_users_24h,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        # Billing aggregates would slot in here; left None so the UI doesn't lie.
        "credits_charged_30d": None,
        "mrr_cents": None,
        "as_of": now.isoformat(),
        "since_30d": last_30d.isoformat(),
    }
