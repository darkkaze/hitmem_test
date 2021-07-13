from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Hit(models.Model):
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
    status = models.CharField(
        max_length=20,
        choices=(('assigned', 'Assigned'),
                 ('failed', 'Failed'),
                 ('completed', 'Completed')),
        default='assigned')
