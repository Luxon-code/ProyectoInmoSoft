from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
def soloAdmin(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Asesor').exists():
            # Usuario pertenece al grupo, redirigir a una página de acceso denegado
            return redirect('/inicioAsesor/') # Cambia la URL según tu caso
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def soloAsesor(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Administrador').exists():
            # Usuario pertenece al grupo, redirigir a una página de acceso denegado
            return redirect('/inicioAdministrador/') # Cambia la URL según tu caso
        return view_func(request, *args, **kwargs)
    return _wrapped_view