from django.urls import path
from . import views

app_name = 'profiles' # <-- Añade esto para nombres de URL con prefijo

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('escenario/<int:pk>/', views.escenario_view, name='escenario'),
    path('final/', views.final_view, name='final'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
]