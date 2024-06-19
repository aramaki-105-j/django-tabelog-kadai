# Generated by Django 4.2.10 on 2024-06-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabelog', '0006_alter_like_unique_together_like_like_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='会社ID')),
                ('name', models.CharField(max_length=100, verbose_name='会社名')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='住所')),
                ('tel', models.CharField(blank=True, max_length=100, null=True, verbose_name='電話番号')),
            ],
        ),
    ]