# Generated by Django 4.0.5 on 2022-06-08 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название рассылки')),
                ('subject', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('message', models.TextField(verbose_name='Текст сообщения')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailing_from', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('to_users', models.ManyToManyField(related_name='mailing_to', to=settings.AUTH_USER_MODEL, verbose_name='Получатели')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]
