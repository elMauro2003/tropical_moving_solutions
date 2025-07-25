# Generated by Django 5.1.7 on 2025-07-11 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0005_remove_contact_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactShort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo electrónico')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('message', models.CharField(max_length=500, verbose_name='Mensaje')),
            ],
        ),
    ]
