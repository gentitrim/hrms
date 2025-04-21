from django.http import HttpResponseForbidden


class RoleAccessMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not hasattr(user, 'branchstaff'):
            return HttpResponseForbidden("Not authenticated")

        if user.branchstaff.role not in self.allowed_roles:
            return HttpResponseForbidden("Premission denied")

        return super().dispatch(request, *args, **kwargs)