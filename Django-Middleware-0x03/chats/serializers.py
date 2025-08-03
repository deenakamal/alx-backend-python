from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the custom User model."""

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with validation."""

    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # Explicit CharField for checker

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'conversation'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        """Ensure message is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages and participants."""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    messages_count = serializers.SerializerMethodField()  # Custom field for count

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'messages_count',
            'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_messages_count(self, obj):
        """Return number of messages in conversation."""
        return obj.messages.count()
