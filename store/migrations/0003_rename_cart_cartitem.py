# Generated by Django 4.2.15 on 2025-03-03 13:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_bike_image_alter_bike_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='CartItem',
        ),
    ]
