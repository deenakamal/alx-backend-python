from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access or modify messages within that conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # obj could be a Message or Conversation — adjust logic:
        # If obj is a Message, check obj.conversation participants
        # If obj is a Conversation, check obj.participants
        if hasattr(obj, 'conversation'):  # It's a Message
            conversation = obj.conversation
        else:  # It's a Conversation
            conversation = obj

        # Ensure user is participant
        return request.user in conversation.participants.all()
