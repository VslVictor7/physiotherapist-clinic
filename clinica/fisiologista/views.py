from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from user.models import User
from .models import Appointment, Fisioterapist
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
      return render(request, 'signup.html')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('cell')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        adress = request.POST.get('adress')
        cep = request.POST.get('cep')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('nome de usuário já existente')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            cpf=cpf,
            phone=phone,
            birth=birth,
            gender=gender,
            adress=adress,
            cep=cep
        )
        user.save()

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login_user(request, authenticated_user)
            return redirect('profile')
        else:
            return HttpResponse('Falha na autenticação')

def login(request):

    if request.method == "GET":
        return render(request, 'login.html')
    else:

        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_user(request, user)
            if Fisioterapist.objects.filter(user=user).exists():
                return redirect('profile-professional')
            return redirect('profile')
        else:
            return HttpResponse('email ou senha invalidos')


@login_required(login_url='/login/')
def profile(request):

    user = request.user


    if request.method == "GET":

      appointments = Appointment.objects.filter(client=user)
      is_professional = Fisioterapist.objects.filter(user=user).exists()

      return render(request, 'profile.html', {'user': user, 'is_professional': is_professional, 'appointments': appointments})
    else:

        data = request.POST.get('data')
        time = request.POST.get('time')
        tipo_tratamento = request.POST.get('tipo_tratamento')
        professional = request.POST.get('professional')
        description = request.POST.get('reason')
        client = user

        agenda = Appointment.objects.filter(data=data, time=time).first()

        if agenda:
            return HttpResponse('Consulta ocupada')

        agenda = Appointment.objects.create(
            client=client,
            data=data,
            time=time,
            tipo_tratamento=tipo_tratamento,
            professional=professional,
            resumo_problemas=description,
        )

        agenda.save()

        return redirect('profile')


@login_required(login_url='/login/')
def profile_professional(request):

    user = request.user


    if request.method == "GET":

      is_professional = Fisioterapist.objects.filter(user=user).exists()

      if is_professional:

            fisioterapist = Fisioterapist.objects.get(user=user)

            appointments = Appointment.objects.exclude(professional=fisioterapist)
      else:

            appointments = Appointment.objects.all()

      return render(request, 'profile_professional.html', {'user': user, 'is_professional': is_professional, 'appointments': appointments})
    else:

        return redirect('profile')

def associar_profissional(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    fisioterapist = get_object_or_404(Fisioterapist, user=request.user)

    appointment.fisioterapist = fisioterapist
    appointment.save()

    return redirect('profile-professional')


def Logout(request):
    logout(request)
    return redirect('home')