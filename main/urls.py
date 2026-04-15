from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('virtual-reception/', views.virtual_reception, name='virtual_reception'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('api/update-reception-id/', views.update_reception_id, name='update_reception_id'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'pics/favicon.ico')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)