from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_403_FORBIDDEN
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages with filtering and pagination
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['message_body']
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Restrict messages to participants of the conversation.
        """
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Restrict to participants
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
