from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse


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
