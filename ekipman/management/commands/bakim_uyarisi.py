from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from ekipman.models import Ekipman
from datetime import timedelta

class Command(BaseCommand):
    help = 'Bakım tarihi yaklaşan ekipmanlar için uyarı gönderir.'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        uyarilacak_tarih = today + timedelta(days=3)  # 3 gün önceden uyarı
        ekipmanlar = Ekipman.objects.filter(bakım_tarihi=uyarilacak_tarih)

        if ekipmanlar.exists():
            for ekipman in ekipmanlar:
                send_mail(
                    subject='Bakım Zamanı Yaklaşıyor!',
                    message=f"{ekipman.adi} ekipmanının bakım zamanı {ekipman.bakım_tarihi} tarihinde dolacak.",
                    from_email=None,
                    recipient_list=['seninmailin@gmail.com'],  # burayı kendi mailinle değiştir
                )
                self.stdout.write(self.style.SUCCESS(f'Uyarı gönderildi: {ekipman.adi}'))
        else:
            self.stdout.write('Yaklaşan bakım tarihi olan ekipman bulunamadı.')
