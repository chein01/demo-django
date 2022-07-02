# Generated by Django 4.0.5 on 2022-07-02 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='pending', max_length=10, verbose_name='Status')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='Description')),
                ('task', models.TextField(verbose_name='Task')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Task',
                'db_table': 'd_task',
            },
        ),
    ]
