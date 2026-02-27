import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session


from api.models.post import Post
from api.models.account import Account
from api.models.schedule import Schedule
from api.models.calendar_item import CalendarItem
from api.models.log import Log
import json

from app.services.linkedin_publisher import publish_linkedin_post
from app.services.linkedin_publisher import publish_linkedin_image_post
from app.services.branding import enrich_post_with_branding



def execute_schedule_db(schedule_id: int, db: Session):
    try:
        # 1️⃣ Obtener schedule
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()

        if not schedule:
            logging.error(f"Schedule {schedule_id} not found")
            return

        # 2️⃣ Obtener calendar_item
        calendar_item = db.query(CalendarItem).filter(
            CalendarItem.id == schedule.calendar_item_id
        ).first()

        if not calendar_item:
            logging.error(f"CalendarItem not found for schedule {schedule_id}")
            return

        # 3️⃣ Obtener post y cuenta
        post = db.query(Post).filter(Post.id == calendar_item.post_id).first()
        account = db.query(Account).filter(Account.id == calendar_item.account_id).first()

        if not post or not account:
            logging.error(f"Post or Account not found for schedule {schedule_id}")
            return

        # 4️⃣ Validar plataforma
        if account.platform != "linkedin":
            logging.info(f"Platform {account.platform} not supported yet")
            return

        if not account.access_token or not account.urn:
            logging.error("LinkedIn account missing token or URN")
            return

        # 5️⃣ Aplicar branding
        final_text = enrich_post_with_branding(post.content)

        # 6️⃣ Publicar en LinkedIn
        if post.media_path:
            status_code, response_text = publish_linkedin_image_post(
            access_token=account.access_token,
            person_urn=account.urn,
            text=final_text,
            image_path=post.media_path
        )
        else:
            status_code, response_text = publish_linkedin_post(
                access_token=account.access_token,
                person_urn=account.urn,
                text=final_text
        )

        # 7️⃣ Evaluar resultado
        if status_code in [200, 201]:

            try:
                response_json = json.loads(response_text)
                linkedin_urn = response_json.get("id")
            except:
                linkedin_urn = None

            post.status = "published"
            post.linkedin_post_urn = linkedin_urn

            schedule.status = "executed"
            schedule.executed_at = datetime.now(timezone.utc)

            log_entry = Log(
                level="info",
                event="schedule_executed",
                message=f"Post published successfully. URN: {linkedin_urn}",
                schedule_id=schedule.id,
                calendar_item_id=calendar_item.id,
                post_id=post.id,
                account_id=account.id
            )

            post.status = "published"
            schedule.status = "executed"
            schedule.executed_at = datetime.now(timezone.utc)

            log_entry = Log(
                level="info",
                event="schedule_executed",
                message="Post published successfully",
                schedule_id=schedule.id,
                calendar_item_id=calendar_item.id,
                post_id=post.id,
                account_id=account.id
            )

            logging.info(f"Schedule {schedule_id} published successfully")

        else:
            schedule.status = "failed"

            log_entry = Log(
                level="error",
                event="schedule_failed",
                message=f"Publishing failed: {response_text}",
                schedule_id=schedule.id,
                calendar_item_id=calendar_item.id,
                post_id=post.id,
                account_id=account.id
            )

            logging.error(f"Schedule {schedule_id} failed: {response_text}")

        db.add(log_entry)
        db.commit()

    except Exception as e:
        db.rollback()
        logging.exception(f"Critical error executing schedule {schedule_id}: {e}")