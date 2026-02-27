import time
import logging
from datetime import datetime, timezone

from db.database import SessionLocal
from api.models.schedule import Schedule
from api.models.calendar_item import CalendarItem
from scheduler.executor import execute_schedule_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    logging.info("Scheduler process started")

    while True:
        db = SessionLocal()

        try:
            now = datetime.now(timezone.utc)

            due_schedules = (
                db.query(Schedule)
                .join(CalendarItem, Schedule.calendar_item_id == CalendarItem.id)
                .filter(
                    Schedule.status == "pending",
                    CalendarItem.scheduled_at <= now
                )
                .all()
            )

            if due_schedules:
                logging.info(f"Found {len(due_schedules)} due schedules")

            for sch in due_schedules:
                logging.info(f"Executing schedule_id={sch.id}")

                try:
                    execute_schedule_db(sch.id, db)
                except Exception as e:
                    db.rollback()
                    logging.exception(f"Schedule failed schedule_id={sch.id}: {e}")

        except Exception as e:
            logging.exception(f"Scheduler loop error: {e}")

        finally:
            db.close()

        time.sleep(10)


if __name__ == "__main__":
    main()