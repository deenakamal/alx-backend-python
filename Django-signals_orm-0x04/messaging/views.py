from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
