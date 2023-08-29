from django.contrib.auth.decorators import user_passes_test


def superuser_required(view_func=None):
    """
    Decorator for views that require superuser status
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
