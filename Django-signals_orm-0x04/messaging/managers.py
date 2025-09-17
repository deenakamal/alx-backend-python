from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """
    def unread_for_user(self, user):
        """
        Returns unread messages for a given user.
        Only fetch necessary fields for optimization.
        """
        return self.filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'content', 'timestamp', 'read')
