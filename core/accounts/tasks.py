"""
Celery task to delete inactive user accounts.

This task identifies user accounts that have been inactive for more than 
7 days (i.e., created more than 7 days ago and marked as inactive) and 
removes them from the database. It logs the number of inactive users found 
and deleted, as well as any errors that may occur during the process.

Procedure:
1. Calculate the date 7 days ago from the current time.
2. Query the database for users who:
   - Were created more than 7 days ago.
   - Are marked as inactive (is_active=False).
3. Log the count of inactive users found.
4. If inactive users are found, delete them in an atomic transaction to ensure 
   database integrity.
5. Log the IDs of the users being deleted and the count of successful 
   deletions.

Error Handling:
- Any exceptions encountered during the process will be logged as errors.

Usage:
This function can be scheduled to run periodically, such as daily, to 
clean up the user database from inactive accounts.

Dependencies:
- Requires Django ORM with a User model defined in the application's models.
- Uses Celery for task scheduling.

Logging:
- The logger will provide information on the number of inactive users 
  found and deleted, as well as warnings for cases with no user IDs 
  to be deleted and errors encountered.

Returns:
- None. However, the function's side effects include deleting users 
  from the database and logging information to the configured logger.
"""

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
