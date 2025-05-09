# Generated by Django 5.1.7 on 2025-05-03 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_and_accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Контактное сообщение',
                'verbose_name_plural': 'Контактные сообщения',
                'ordering': ['-created_at'],
            },
        ),
    ]
