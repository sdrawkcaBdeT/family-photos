from django.shortcuts import redirect
from functools import wraps

def family_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('has_access'):
            return redirect('login')
        if not request.session.get('uploader_name'):
            return redirect('set_name')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
