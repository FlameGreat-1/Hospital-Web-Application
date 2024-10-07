# Generated by Django 5.1.1 on 2024-09-23 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total_appointments', models.IntegerField(default=0)),
                ('pending_appointments', models.IntegerField(default=0)),
                ('completed_appointments', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
