from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from online.models import Usuario

@login_required()
def GestionUsuarios(request):
    Usuarios = Usuario.objects.all()
    if request.method == "POST":
        user = request.POST.get('Userid', False)
        activo = request.POST.get('activo', False)
        admin = request.POST.get('admin', False)
        tecnico = request.POST.get('tecnico', False)
        if admin:
            admin = True
        if activo:
            activo = True
        if tecnico:
            tecnico = True
        print(request.POST.get('Elimnar_user', False))
        userchange = Usuario.objects.get(id=user)
        userchange.admin = admin
        userchange.activo = activo
        userchange.tecnico = tecnico
        userchange.save()
        return redirect('/GestionUsuarios/')
    return render(request, "GestionUsuarios.html",{"Usuarios":Usuarios})
@login_required()
def EliminarUsuario(request,idUser):
    if request.user.admin:
        User = Usuario.objects.get(id=idUser)
        User.delete()
    return redirect('/GestionUsuarios/')
