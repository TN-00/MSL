# Generated by Django 3.2.25 on 2025-07-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0005_alter_signimg_detected_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
