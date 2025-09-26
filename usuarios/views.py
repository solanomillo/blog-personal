from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth.models import User


""" VISTAS PARA EL LOGIN Y REGISTRO DE USUARIOS """

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('/')
    
    pagina = request.GET.get('next', '/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'Bienvenido {usuario.first_name} {usuario.last_name}')
            # Si hay un 'next' en la URL, redirigir a esa página
            if pagina:
                return HttpResponseRedirect(pagina)
            # Redirigir al index si no hay 'next' en la URL
            return redirect('/')          

            
        else:
            messages.error(request, 'Datos incorrectos')
    
    return render(request, 'login.html', {
        'destino': pagina
    })

def logout_view(request):
    ''' vista para el logout de usuarios '''
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('/')

       
def registro(request):
    ''' vista para el registro de usuarios '''
    if request.user.is_authenticated:
        return redirect('/')
    
    dataForm = RegistroForm()
    if request.method == 'POST':
        dataForm = RegistroForm(request.POST or None)
        if dataForm.is_valid():
            # limpiar los datos del formulario
            data = dataForm.cleaned_data
            # Crear el usuario
            nuevoUsuario = User.objects.create_user(
                username=data['nombre'],
                first_name=data['nombre'],
                last_name=data['apellido'],
                email=data['email'],
                password=data['password']
            )
            
            
            # Iniciar sesión automáticamente al usuario
            if nuevoUsuario is not None:
                login(request, nuevoUsuario)
                messages.success(request,f'Bienvenido {nuevoUsuario.first_name} {nuevoUsuario.last_name}')
                return redirect('/')
            
    return render(request, 'registro.html', {
        'form': dataForm
    })       
