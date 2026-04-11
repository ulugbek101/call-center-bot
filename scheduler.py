from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import create_engine
from zoneinfo import ZoneInfo

from loader import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT
from tasks import send_random_motivational_phrase


# -------------------------------------------------
# Timezone
# -------------------------------------------------
TASHKENT_TZ = ZoneInfo("Asia/Tashkent")


# -------------------------------------------------
# JobStore (DB-backed)
# -------------------------------------------------
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,   # detects dead connections
    pool_recycle=1800,    # recycle every 30 min
    pool_size=5,
    max_overflow=10,
)

jobstores = {
    "default": SQLAlchemyJobStore(engine=engine)
}

job_defaults = {
    "coalesce": True,
    "misfire_grace_time": 600,  # 10 minutes
}

scheduler = AsyncIOScheduler(
    timezone=TASHKENT_TZ,
    jobstores=jobstores,
    job_defaults=job_defaults,
)


def start_scheduler():
    """
    Starts APScheduler and registers all cron jobs.
    Safe to call multiple times (jobs won't duplicate).
    """
    if scheduler.running:
        return

    scheduler.start()

    scheduler.add_job(
        send_random_motivational_phrase,
        trigger="cron",
        hour=10,
        minute=00,
        id="send_random_motivational_phrase",
        replace_existing=True,
    )
