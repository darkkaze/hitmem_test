from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Hit(models.Model):
    """
    notes:
        managed_by maybe is not necesary because a hitmen have a manager
        but bigboss can change the hitmen...
        the backlog don't delve into these use cases
    """
    target = models.CharField(max_length=100)
    description = models.TextField()
    managed_by = models.ForeignKey(
        User,
        related_name='created_hits',
        on_delete=models.PROTECT)
    hitmen_by = models.ForeignKey(
        User,
        related_name='assigned_hits',
        on_delete=models.PROTECT)
    created_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=(('assigned', 'Assigned'),
                 ('failed', 'Failed'),
                 ('completed', 'Completed')),
        default='assigned')
