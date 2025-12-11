from django.apps import apps

def log_activity(user, action, description=""):
    """
    Log a user activity to the ActivityLog model.
    Safe to call even if activity_logs app is not loaded.
    """
    try:
        ActivityLog = apps.get_model('activity_logs', 'ActivityLog')
        ActivityLog.objects.create(
            user=user,
            action=action,
            description=description
        )
    except Exception as e:
        # Silently fail if activity logging is unavailable
        # (don't block main action if logging fails)
        pass
