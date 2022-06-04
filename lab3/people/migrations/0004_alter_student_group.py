# Generated by Django 4.0.5 on 2022-06-04 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
        ('people', '0003_alter_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='diary.group', verbose_name='Состоит в группе'),
        ),
    ]
