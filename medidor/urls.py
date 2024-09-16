from django.urls import path
from . import views

urlpatterns = [
    path('contador/', views.contador_view, name='contador'),
    path('ver-datos/', views.ver_datos_agua, name='ver_datos'),
    path('consumo/', views.promedio_consumo_view, name='promedio_consumo_view'),  # Nueva URL
    path('establecer-limite/', views.establecer_límite_view, name='establecer_límite_view'),

]
