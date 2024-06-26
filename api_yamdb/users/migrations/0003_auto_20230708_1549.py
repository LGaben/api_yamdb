# Generated by Django 3.2 on 2023-07-08 12:49

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230705_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем или с таким емейлом уже существует'}, help_text='Не больше 150 символов.Только буквы, цифры и @/./+/-/_', max_length=150, unique=True, validators=[users.validators.validate_username], verbose_name='Пользователь'),
        ),
    ]
