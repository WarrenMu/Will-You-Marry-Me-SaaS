import uuid

from django.db import models
from django.utils import timezone


class Proposal(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    proposer_name = models.CharField(max_length=120, blank=True)
    proposee_name = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def respond(self, response: str) -> None:
        if response not in (self.Status.ACCEPTED, self.Status.REJECTED):
            raise ValueError('Response must be accepted or rejected')

        if self.status != self.Status.PENDING:
            # Only allow a single response for this simple MVP.
            raise ValueError('Proposal has already been responded to')

        self.status = response
        self.responded_at = timezone.now()
        self.save(update_fields=['status', 'responded_at'])
