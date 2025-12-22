from django.conf import settings
from .models import Notification

def create_notification(recipient, notification_type, message, sender=None, related_object=None):
    """
    Create a notification for a user
    """
    # Handle recipient input (could be User object, user ID, or username)
    from django.contrib.auth import get_user_model
    User = get_user_model()  # This gets your CustomUser model
    
    if isinstance(recipient, User):
        recipient_user = recipient
    else:
        # Try to get by ID
        try:
            if isinstance(recipient, int) or recipient.isdigit():
                recipient_user = User.objects.get(id=recipient)
            else:
                # Assume it's a username
                recipient_user = User.objects.get(username=recipient)
        except (User.DoesNotExist, ValueError, AttributeError):
            # If we can't find the user, return None
            return None
    
    # Handle sender input
    sender_user = None
    if sender:
        if isinstance(sender, User):
            sender_user = sender
        else:
            try:
                if isinstance(sender, int) or (isinstance(sender, str) and sender.isdigit()):
                    sender_user = User.objects.get(id=sender)
                else:
                    sender_user = User.objects.get(username=sender)
            except (User.DoesNotExist, ValueError, AttributeError):
                sender_user = None
    
    # Create the notification
    notification = Notification.objects.create(
        recipient=recipient_user,
        sender=sender_user,
        notification_type=notification_type,
        message=message,
        is_read=False
    )
    
    if related_object:
        notification.related_object_id = related_object.id
        notification.related_object_type = related_object.__class__.__name__
        notification.save()
    
    return notification


# Additional helper functions you might find useful:

def create_bulk_notifications(recipients, notification_type, message, sender=None, related_object=None):
    """
    Create notifications for multiple users at once
    """
    notifications = []
    for recipient in recipients:
        notification = create_notification(
            recipient=recipient,
            notification_type=notification_type,
            message=message,
            sender=sender,
            related_object=related_object
        )
        if notification:
            notifications.append(notification)
    return notifications


def create_system_notification(recipient, message, related_object=None):
    """
    Create a system notification (no sender)
    """
    return create_notification(
        recipient=recipient,
        notification_type='system',
        message=message,
        sender=None,
        related_object=related_object
    )


def get_unread_notifications(user):
    """
    Get all unread notifications for a user
    """
    return Notification.objects.filter(recipient=user, is_read=False)


def mark_notifications_as_read(user, notification_ids=None):
    """
    Mark notifications as read for a user
    If notification_ids is None, mark all as read
    """
    queryset = Notification.objects.filter(recipient=user, is_read=False)
    
    if notification_ids:
        queryset = queryset.filter(id__in=notification_ids)
    
    updated_count = queryset.update(is_read=True)
    return updated_count