# Generated migration to remove copias field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='copias',
        ),
    ]
