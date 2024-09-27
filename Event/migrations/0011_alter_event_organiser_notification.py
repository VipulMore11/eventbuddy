# Generated by Django 5.1.1 on 2024-09-27 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
        ('Event', '0010_alter_birthdaydetails_event_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.organiser'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('notification_type', models.CharField(choices=[('invitation', 'Invitation'), ('normal', 'Normal')], max_length=20)),
                ('is_seen', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.organiser')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
