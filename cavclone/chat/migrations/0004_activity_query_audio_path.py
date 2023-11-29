# Generated by Django 4.2.7 on 2023-11-28 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_query_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='query',
            name='audio_path',
            field=models.TextField(default='/cavclone/output.mp3'),
            preserve_default=False,
        ),
    ]
