from django.conf import settings
from .models import Notification

User = settings.AUTH_USER_MODEL

def notifications_context(request):
    context = {}
    if request.user.is_authenticated:
        context['unread_notifications_count'] = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
    return context