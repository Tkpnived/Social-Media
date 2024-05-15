# Generated by Django 3.1.10 on 2024-01-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0009_updb_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('likes', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='updb',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
