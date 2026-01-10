from django.core.exceptions import PermissionDenied
from django.http import HttpRequest


class UserIsOwnerMixin(object):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != self.request.user:  # було ==
            raise PermissionDenied  # був return
        return super().dispatch(request, *args, **kwargs)


class UserIsAuthorMixin(object):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:  # було ==
            raise PermissionDenied  # був return
        return super().dispatch(request, *args, **kwargs)
