# Generated by Django 5.2.3 on 2025-06-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekipman', '0002_ekipman_dosya'),
    ]

    operations = [
        migrations.AddField(
            model_name='ekipman',
            name='qr_kod',
            field=models.ImageField(blank=True, null=True, upload_to='qr_kodlar/'),
        ),
    ]
