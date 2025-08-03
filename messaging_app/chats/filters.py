import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    # Filter by sender user ID
    sender = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')
    # Filter by content keyword
    message_body = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    # Filter by time range
    created_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'message_body', 'created_after', 'created_before']
        