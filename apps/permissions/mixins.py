import logging

from django.core.exceptions import PermissionDenied
from django.utils import timezone

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PermissionMixin():
    """
    manage the permission in general and granular objects.

    notes:
        based on django-rest-framework permission system

    usage:
        class SomeView(View, PermissionMixin):
            permission_classes = [IsAuthenticated]
    """

    permission_classes = []

    def permission_denied(self, request, message=None, code=None):
        if code and message:
            logger.warning(
                f'code: {code} detail: {message}')
        raise PermissionDenied()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        return [permission() for permission in self.permission_classes]

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_object_permissions(self, request, obj):
        """
        Check if the request should be permitted for a given object.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def get_object(self):
        """
        check object permissions.

        notes:
            details from  django.views.generic use this method 
            for get a single object
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def setup(self, request, *args, **kwargs):
        """
        check permissions.

        notes:
            all django.views.generic run this method for process a request
        """
        self.check_permissions(request)
        super().setup(request, *args, **kwargs)
