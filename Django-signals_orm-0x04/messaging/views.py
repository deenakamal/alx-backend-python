from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Message
from django.views.decorators.cache import cache_page

User = get_user_model()


@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their own account.
    When the user confirms deletion via POST request, the user object
    is deleted, which triggers post_delete signals for cleanup.
    """
    user = request.user
    if request.method == "POST":
        user.delete()  # Triggers post_delete signal to remove related data
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")  # Redirect after deletion

    return render(request, "messaging/delete_user.html")  # Confirmation page


@login_required
def threaded_conversations(request):
    # Fetch root messages (no parent) for current user
    root_messages = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver') \
     .prefetch_related('replies__sender', 'replies__receiver')

    # Recursive function to build nested thread
    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    data = [build_thread(msg) for msg in root_messages]
    return JsonResponse(data, safe=False)


@login_required
def unread_inbox(request):
    """
    Display only unread messages for the logged-in user.
    Optimized with .only() to fetch only necessary fields.
    """
    user = request.user

    # Fetch unread messages using custom manager
    # Apply .only() here to optimize query
    unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp', 'read')

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })
    

@login_required
@cache_page(60)
def conversation_messages(request, conversation_id):
    """
    Returns messages in a specific conversation (threaded) as JSON.
    Cached for 60 seconds.
    """
    user = request.user
    # Fetch root messages for this conversation
    root_messages = Message.objects.filter(
        parent_message__isnull=True,
        receiver=user
    ).filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver') \
      .prefetch_related('replies__sender', 'replies__receiver')

    def build_thread(message):
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "read": message.read,
            "replies": [build_thread(reply) for reply in message.replies.all()]
        }

    data = [build_thread(msg) for msg in root_messages]
    return JsonResponse(data, safe=False)