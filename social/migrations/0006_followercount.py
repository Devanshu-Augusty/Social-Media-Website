# Generated by Django 4.1.7 on 2023-03-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
            ],
        ),
    ]
