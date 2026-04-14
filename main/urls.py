from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('virtual-reception/', views.virtual_reception, name='virtual_reception'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('api/update-reception-id/', views.update_reception_id, name='update_reception_id'),
]