# Generated by Django 4.0 on 2022-02-03 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='position',
            field=models.CharField(choices=[('선택', '선택'), ('개발', '개발'), ('기획', '기획'), ('디자인', '디자인')], default='선택', max_length=10),
        ),
    ]
