# Generated by Django 3.2 on 2023-07-08 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_comment_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Комментарии'),
            preserve_default=False,
        ),
    ]
