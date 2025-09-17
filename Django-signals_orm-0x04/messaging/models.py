from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# -----------------------------
# Message Model
# -----------------------------
class Message(models.Model):
    """
    Message model to store messages between users.
    Supports threaded conversations using a self-referential foreign key.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # Self-referential FK for replies (threaded messages)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

# -----------------------------
# Notification Model
# -----------------------------
class Notification(models.Model):
    """
    Notification model to store alerts for users when they receive a message.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"

# -----------------------------
# MessageHistory Model
# -----------------------------
class MessageHistory(models.Model):
    """
    Stores the old content of a message before it is edited.
    Keeps track of who edited the message (edited_by).
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Keep history even if editor is deleted
        null=True,
        blank=True,
        related_name='edited_messages'
    )

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
