from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access.
    - Only participants of the conversation can view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get conversation from object
        conversation = getattr(obj, 'conversation', obj)

        # Allow only participants
        if request.user not in conversation.participants.all():
            return False

        # Explicitly check allowed methods for updates/deletes
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Only participants allowed to modify
            return request.user in conversation.participants.all()

        # Allow safe methods (GET) and POST for participants
        return True
