from django.urls import path
from . import views

urlpatterns = [
    path('contador/', views.contador_view, name='contador'),
    path('ver-datos/', views.ver_datos_agua, name='ver_datos'),
    path('promedio-consumo/', views.promedio_consumo_view, name='promedio_consumo'),  # Nueva URL
]
