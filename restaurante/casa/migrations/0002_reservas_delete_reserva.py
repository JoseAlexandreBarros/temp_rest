# Generated by Django 4.2.2 on 2023-07-31 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('horarios', models.CharField(choices=[('TR', 'Tarde'), ('MN', 'Manhã'), ('NO', 'Noite')], max_length=2)),
                ('locais', models.CharField(choices=[('CN', 'Centro'), ('PR', 'Periferia')], max_length=2)),
                ('data_reserva', models.IntegerField(default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Reserva',
        ),
    ]