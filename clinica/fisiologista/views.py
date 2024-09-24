from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from user.models import User
from .models import Appointment, Fisioterapist
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, LoginForm, AppointmentForm

def home(request):
    return render(request, 'index.html')

class Register(CreateView):
    template_name = 'cadastro.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('fisiologista:login')

    def form_valid(self, form):
        user = form.save(commit=True)
        return super().form_valid(form)

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'fisioterapist'):
            return reverse_lazy('fisiologista:profile-professional')
        return reverse_lazy('fisiologista:profile')


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile_patient.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('fisiologista:profile')
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['appointments'] = Appointment.objects.filter(client=user)
        context['is_professional'] = Fisioterapist.objects.filter(user=user).exists()
        return context

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data['data']
        time = form.cleaned_data['time']
        tipo_tratamento = form.cleaned_data['tipo_tratamento']
        professional = form.cleaned_data['professional']
        description = form.cleaned_data['resumo_problemas']
        client = user

        agenda = Appointment.objects.filter(data=data, time=time).first()
        if agenda:
            return HttpResponse('Consulta ocupada')

        Appointment.objects.create(
            client=client,
            data=data,
            time=time,
            tipo_tratamento=tipo_tratamento,
            professional=professional,
            resumo_problemas=description,
        )

        return super().form_valid(form)

class ProfileProfessionalView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_professional.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        is_professional = Fisioterapist.objects.filter(user=user).exists()
        context['is_professional'] = is_professional

        if is_professional:
            fisioterapist = Fisioterapist.objects.get(user=user)
            context['appointments'] = Appointment.objects.exclude(professional=fisioterapist)
        else:
            context['appointments'] = Appointment.objects.all()

        return context

class Edit(UpdateView):
    template_name = 'edit.html'
    model = Appointment
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse_lazy('fisiologista:profile')

    def form_valid(self, form):
        user = form.save(commit=True)
        return super().form_valid(form)

def delete(request, pk):
    treino = Appointment.objects.get(pk=pk)
    treino.delete()
    return redirect('fisiologista:profile')

def associar_profissional(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    professional = get_object_or_404(Fisioterapist, user=request.user)
    appointment.professional = professional
    appointment.save()
    return redirect('fisiologista:profile-professional')

def desassociar_profissional(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.professional = None
    appointment.save()
    return redirect('fisiologista:profile-professional')

def Logout(request):
    logout(request)
    return redirect('fisiologista:home')