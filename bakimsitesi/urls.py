from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.contrib import admin
from django.urls import path
from ekipman import views as ekipman_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False)),
    path('admin/', admin.site.urls),
    path('gorevlerim/', ekipman_views.teknisyen_gorevleri, name='teknisyen_gorevleri'),
    path('tamamlanan-gorevler/', ekipman_views.tamamlanan_gorevler, name='tamamlanan_gorevler'),
    path('gorev/<int:gorev_id>/tamamla/', ekipman_views.gorev_tamamla, name='gorev_tamamla'),
    path('qr/<int:pk>/', ekipman_views.qr_ekipman_bilgi, name='qr_ekipman_bilgi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
