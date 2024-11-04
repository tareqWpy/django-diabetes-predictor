import datetime
import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import User

logger = logging.getLogger(__name__)


@shared_task
def delete_inactive_users():
    try:
        # Calculate the date 7 days ago
        seven_days_ago = timezone.now() - datetime.timedelta(days=7)

        # Filter for inactive users created more than 7 days ago
        inactive_users = User.objects.filter(
            created_date__lt=seven_days_ago, is_active=False
        )

        # Get the count of inactive users
        inactive_count = inactive_users.count()

        # Log the number of inactive users found
        if inactive_count == 1:
            logger.info("Found 1 inactive user.")
        else:
            logger.info(f"Found {inactive_count} inactive users.")

        # Get the IDs of the inactive users to delete
        user_ids = list(inactive_users.values_list("id", flat=True))
        logger.info("Deleting users with IDs: %s", user_ids)

        if user_ids:
            with transaction.atomic():
                count, _ = User.objects.filter(id__in=user_ids).delete()
                if count == 1:
                    logger.info("1 user deleted.")
                else:
                    logger.info("%d users deleted.", count)
        else:
            logger.warning("No user IDs provided for deletion.")
    except Exception as e:
        logger.error("Error deleting users: %s", str(e))
