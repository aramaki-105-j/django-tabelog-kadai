# Generated by Django 4.2.10 on 2024-06-07 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabelog', '0003_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]