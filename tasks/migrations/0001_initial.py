# Generated by Django 4.0.6 on 2022-07-17 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tgbot', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('priority', models.IntegerField(default=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgbot.user')),
            ],
        ),
    ]
