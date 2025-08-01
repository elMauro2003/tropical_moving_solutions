# Generated by Django 5.1.7 on 2025-07-10 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_index=True, max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('display_name', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('query', 'display_name')},
            },
        ),
    ]
