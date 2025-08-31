from django.urls import path
from . import views

app_name = 'profiles' 

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('escenario/<int:pk>/', views.escenario_view, name='escenario'),
    path('final/', views.final_view, name='final'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('glosario/', views.glosario_view, name='glosario'), 
    path('perfil/', views.perfil_view, name='perfil'),
]