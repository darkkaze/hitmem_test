class OperationHolderMixin:
    def __and__(self, other):
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        return OperandHolder(OR, self, other)


class OperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class, op2_class):
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class AND:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, request, view):
        return (
            self.op1.has_permission(request, view) and
            self.op2.has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.op1.has_object_permission(request, view, obj) and
            self.op2.has_object_permission(request, view, obj)
        )


class OR:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, request, view):
        return (
            self.op1.has_permission(request, view) or
            self.op2.has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.op1.has_object_permission(request, view, obj) or
            self.op2.has_object_permission(request, view, obj)
        )


class BasePermissionMetaclass(OperationHolderMixin, type):
    """
    Taked and simplified from django-rest-framework.permissions
    """
    pass


class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
