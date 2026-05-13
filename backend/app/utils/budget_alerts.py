"""Budget alert system for monitoring daily spend."""

from datetime import datetime, timedelta
from typing import Optional

from app.db.client import get_supabase_admin_client
from app.config import settings


async def check_daily_budget(user_id: Optional[str] = None) -> dict:
    """
    Check if daily spend has exceeded budget threshold.

    Args:
        user_id: Optional user filter

    Returns:
        Dictionary with alert status and spending details
    """
    try:
        supabase = get_supabase_admin_client()

        # Get today's spending
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        query = supabase.table("research_sessions").select(
            "cost_usd,user_id"
        ).gte("created_at", today_start.isoformat()).lt(
            "created_at", today_end.isoformat()
        )

        if user_id:
            query = query.eq("user_id", user_id)

        result = query.execute()

        # Calculate total spend
        total_spend = sum(s.get("cost_usd", 0) or 0 for s in result.data)

        # Check against threshold
        threshold = settings.daily_spend_alert_usd
        alert_triggered = total_spend >= threshold

        alert_info = {
            "alert_triggered": alert_triggered,
            "total_spend_usd": round(total_spend, 6),
            "threshold_usd": threshold,
            "percentage_used": round((total_spend / threshold * 100), 2) if threshold > 0 else 0,
            "remaining_budget_usd": max(0, threshold - total_spend),
            "date": today_start.date().isoformat(),
        }

        if alert_triggered:
            print(f"[BUDGET_ALERT] Daily spend ${total_spend:.6f} exceeded threshold ${threshold:.2f}")
            # TODO v0.13: Send email notification
            # await send_budget_alert_email(alert_info)

        return alert_info

    except Exception as e:
        print(f"[BUDGET_ALERT] Error checking budget: {str(e)}")
        return {
            "alert_triggered": False,
            "error": str(e),
        }


async def send_budget_alert_email(alert_info: dict):
    """
    Send budget alert email notification.

    TODO v0.13: Implement email sending via SendGrid or similar service.

    Args:
        alert_info: Alert details to include in email
    """
    # Placeholder for email integration
    print(f"[EMAIL] Budget alert would be sent: {alert_info}")
    # Example implementation:
    # import sendgrid
    # sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
    # message = {
    #     "to": settings.admin_email,
    #     "from": "alerts@research-assistant.com",
    #     "subject": f"Budget Alert: ${alert_info['total_spend_usd']:.2f} spent today",
    #     "text": f"Daily spend has exceeded threshold of ${alert_info['threshold_usd']:.2f}"
    # }
    # sg.send(message)
    pass


async def log_budget_check(session_id: str):
    """
    Check budget after a query completes and log if alert triggered.

    This is called as a post-query hook to monitor spending.

    Args:
        session_id: The research session ID that just completed
    """
    alert_info = await check_daily_budget()

    if alert_info.get("alert_triggered"):
        print(f"[BUDGET_ALERT] Triggered for session {session_id}")
        # Log to a budget_alerts table if needed
        # For now, just print - email integration in future version
