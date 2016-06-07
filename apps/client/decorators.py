from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.conf import settings;



def user_agent_test(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.META['HTTP_USER_AGENT'] != 'SimpleNect':
                if settings.DEBUG is False:
                    return HttpResponseNotFound('<h1>404 Page not found</h1>')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def sn_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_agent_test(
        lambda u: u
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.META['HTTP_USER_AGENT'] != 'SimpleNect':
            	if settings.DEBUG is False:
                    return HttpResponseNotFound('<h1>404 Page not found</h1>')
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponse("401", status=401)
        return _wrapped_view
    return decorator


def snlogin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


