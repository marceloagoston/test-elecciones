from django.core.exceptions import PermissionDenied


class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        """Chequear si el usuario tiene permisos para acceder a la view segun el rol
        Flujo:
            - Solo Admin puede acceder al dashboard
            - Demas tipos de usuario recibiran una respuesta 403 al intentar acceder
            a las views del Admin
        Return
            - PermissionDenied si no tiene permisos
            - El mixin finaliza y sigue con el dispatch siguiente de la clase
        """
        for gr in request.user.groups.all():
            if gr.name == 'admin':
                return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
