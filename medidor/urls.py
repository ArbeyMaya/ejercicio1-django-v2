from django.urls import path
from . import views

urlpatterns = [
    path('contador/', views.contador_view, name='contador'),
    path('consumo/', views.promedio_consumo_view, name='promedio_consumo_view'),  # Nueva URL
    path('limite/', views.establecer_límite_view, name='establecer_límite_view'),
    
]
