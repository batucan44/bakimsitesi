from django.db import models
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User

# EKİPMAN MODELİ
class Ekipman(models.Model):
    adi = models.CharField(max_length=100)
    bulunduğu_yer = models.CharField(max_length=200)
    bakım_tarihi = models.DateField()
    muayene_tarihi = models.DateField()
    kontrol_tarihi = models.DateField()
    dosya = models.FileField(upload_to="ekipman_dosyalar/", null=True, blank=True)
    qr_kod = models.ImageField(upload_to="qr_kodlar/", blank=True, null=True)

    def __str__(self):
        return self.adi

    def get_absolute_url(self):
        return reverse("ekipman_detay", args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Önce kaydı yaparak ID'nin oluşmasını sağla
        super().save(*args, **kwargs)

        # QR kod verisini oluştur
        qr_data = f"https://bakimsitesi.onrender.com/qr/{self.id}/"
        qr_img = qrcode.make(qr_data)

        # QR kodu belleğe kaydet
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)  # İmleci başa al, bu çok önemli!

        filename = f"qr_{self.id}.png"

        # QR kodu modele ekle (save=False ile tekrar sonsuz döngüyü engelle)
        self.qr_kod.save(filename, File(buffer), save=False)

        # QR kod ile birlikte kaydet
        super().save(*args, **kwargs)


# GÖREV MODELİ
class Gorev(models.Model):
    ekipman = models.ForeignKey(Ekipman, on_delete=models.CASCADE)
    teknisyen = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'Teknisyen'}  # sadece Teknisyen grubundakiler listelenir
    )
    aciklama = models.TextField(blank=True, null=True)
    durum = models.CharField(max_length=20, choices=[
        ('atanmis', 'Atanmış'),
        ('tamamlandi', 'Tamamlandı'),
    ], default='atanmis')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ekipman.adi} - {self.teknisyen.username} - {self.durum}"


# QR SORGU KAYDI MODELİ
class QRSorguKaydi(models.Model):
    ekipman = models.ForeignKey(Ekipman, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_adresi = models.GenericIPAddressField()
    sorgulama_zamani = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ekipman.adi} - {self.kullanici or 'Anonim'} - {self.sorgulama_zamani}"