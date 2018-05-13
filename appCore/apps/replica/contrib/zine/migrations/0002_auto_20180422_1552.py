# Generated by Django 2.0 on 2018-04-22 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import replica.contrib.zine.models


class Migration(migrations.Migration):

    dependencies = [
        ('zine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulse.Media'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(default=replica.contrib.zine.models.DefaultUser, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='collections', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='promoted',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pulse.Media'),
        ),
        migrations.AlterField(
            model_name='promoted',
            name='user',
            field=models.ForeignKey(default=replica.contrib.zine.models.DefaultUser, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='promoted_entries', to=settings.AUTH_USER_MODEL),
        ),
    ]