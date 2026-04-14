from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('virtual-reception/', views.virtual_reception, name='virtual_reception'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('api/update-reception-id/', views.update_reception_id, name='update_reception_id'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)