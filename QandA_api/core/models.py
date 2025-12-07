from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from datetime import datetime
import uuid


class Question(models.Model):
    text: str = models.TextField(
        validators=[MinLengthValidator(1)]
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text[:50]

    def clean(self):
        if not self.text.strip():
            raise ValidationError("Question text cannot be empty.")
        if len(self.text) > 1000:
            raise ValidationError("Question text is too long (max 1000 characters).")


class Answer(models.Model):
    question: Question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user_id: int = models.CharField(
        max_length=36,
        validators=[MinLengthValidator(36)]
    )
    text: str = models.TextField(
        validators=[MinLengthValidator(1)]
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Answer by {self.user_id}: {self.text[:50]}"

    def clean(self):
        if not self.text.strip():
            raise ValidationError("Answer text cannot be empty.")
        if len(self.text) > 2000:
            raise ValidationError("Answer text is too long (max 2000 characters).")
        try:
            uuid.UUID(self.user_id)
        except ValueError:
            raise ValidationError("user_id must be a valid UUID.")
