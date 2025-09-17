from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

# -----------------------------
# Notification on new message
# -----------------------------
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Automatically create a notification for the receiver when
    a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# -----------------------------
# Message edit history
# -----------------------------
@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    """
    Before a message is saved, check if its content changed.
    If so, save the old content in MessageHistory and mark edited=True.
    """
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.sender  # consider using current user if available
            )
            instance.edited = True

# -----------------------------
# Cleanup on user deletion
# -----------------------------
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Automatically delete all messages, notifications, and message history
    associated with the deleted user.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()

