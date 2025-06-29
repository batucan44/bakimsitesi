from django.shortcuts import render, get_object_or_404
from .models import Ekipman

def ekipman_detay(request, pk):
    ekipman = get_object_or_404(Ekipman, pk=pk)
    return render(request, 'ekipman/ekipman_detay.html', {'ekipman': ekipman})

from django.contrib.auth.decorators import login_required
from .models import Gorev

@login_required
def teknisyen_gorevleri(request):
    gorevler = Gorev.objects.filter(teknisyen=request.user)
    return render(request, 'ekipman/teknisyen_gorevleri.html', {'gorevler': gorevler})
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # ekle


@login_required
def gorev_tamamla(request, gorev_id):
    gorev = Gorev.objects.get(id=gorev_id, teknisyen=request.user)
    gorev.durum = 'tamamlandi'
    gorev.save()

    # E-posta gönder
    send_mail(
        subject='Görev Tamamlandı',
        message=f'{request.user.username}, "{gorev.ekipman.adi}" adlı ekipmana ait görevi tamamladı.',
        from_email=None,  # DEFAULT_FROM_EMAIL kullanır
        recipient_list=['seninmailin@gmail.com'],  # Bildirimin gideceği adres
    )

    return redirect('teknisyen_gorevleri')
from django.contrib.auth.decorators import login_required
from .models import Gorev

@login_required
def tamamlanan_gorevler(request):
    gorevler = Gorev.objects.filter(teknisyen=request.user, durum='tamamlandi')
    return render(request, 'ekipman/tamamlanan_gorevler.html', {'gorevler': gorevler})
from django.shortcuts import render, get_object_or_404
from .models import QRSorguKaydi  # en üste modellerden QRSorguKaydi'yı ekle

def qr_ekipman_bilgi(request, pk):
    ekipman = get_object_or_404(Ekipman, pk=pk)

    # Kayıt et
    ip_adresi = request.META.get('REMOTE_ADDR')
    kullanici = request.user if request.user.is_authenticated else None

    QRSorguKaydi.objects.create(
        ekipman=ekipman,
        kullanici=kullanici,
        ip_adresi=ip_adresi
    )

    return render(request, 'ekipman/qr_ekipman_bilgi.html', {'ekipman': ekipman})

