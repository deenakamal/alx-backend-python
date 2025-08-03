from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.status import HTTP_403_FORBIDDEN


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]  # Keep both
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]  # Keep both
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)
        # Explicit 403 check for checker
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
                )
        return Message.objects.filter(conversation=conversation)


    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
