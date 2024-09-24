from django.urls import path
from . import views
from .views import Register, Login, ProfileView, ProfileProfessionalView, Edit, delete

app_name = 'fisiologista'

urlpatterns = [
    path('', views.home, name="home"),
    path('registro/', Register.as_view(), name="registro"),
    path('login/', Login.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile-professional/', ProfileProfessionalView.as_view(), name="profile-professional"),
    path('logout/', views.Logout, name="logout"),
    path('edit-appointment/<int:pk>/', Edit.as_view(), name='edit'),
    path('delete-appointment/<int:pk>/', delete, name='delete'),
    path('associar-profissional/<int:appointment_id>/', views.associar_profissional, name='associar_profissional'),
    path('desassociar-profissional/<int:appointment_id>/', views.desassociar_profissional, name='desassociar_profissional'),
]