from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
def threaded_conversation(request):
    """
    Fetch top-level messages for the logged-in user (as sender or receiver)
    along with their replies.
    Uses select_related and prefetch_related to optimize queries.
    """
    user = request.user

    # Fetch top-level messages where the current user is sender or receiver
    top_messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user),
        parent_message__isnull=True
    ).select_related('sender', 'receiver') \
     .prefetch_related('replies__sender', 'replies__receiver')

    # Recursive function to get all replies
    def get_replies(message):
        return [
            {
                'id': reply.id,
                'sender': reply.sender.username,
                'receiver': reply.receiver.username,
                'content': reply.content,
                'timestamp': reply.timestamp,
                'replies': get_replies(reply)
            }
            for reply in message.replies.all()
        ]

    # Prepare conversation data for template
    conversation_data = []
    for msg in top_messages:
        conversation_data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'timestamp': msg.timestamp,
            'replies': get_replies(msg)
        })

    return render(request, 'messaging/threaded_conversation.html', {
        'conversation_data': conversation_data
    })
