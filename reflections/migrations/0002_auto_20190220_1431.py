# Generated by Django 2.1.5 on 2019-02-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reflections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='reflection',
            name='tags',
        ),
        migrations.AddField(
            model_name='tags',
            name='reflection',
            field=models.ManyToManyField(to='reflections.Reflection'),
        ),
    ]
