"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.home_view, name='home'),  # Strona główna
    path('add/', views.add_market_data, name='add_market_data'),  # Wprowadzenie danych rynkowych
    path('export/', views.export_to_csv, name='export_to_csv'),  # Eksport do CSV
]