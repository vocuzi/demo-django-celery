# Generated by Django 3.0.8 on 2020-07-27 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_auto_20200727_0535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samplemodelforexport',
            name='email',
        ),
        migrations.RemoveField(
            model_name='samplemodelforexport',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='samplemodelforexport',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='samplemodelforexport',
            name='last_name',
        ),
        migrations.AddField(
            model_name='samplemodelforexport',
            name='batch_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='task_app.HistoricRuns'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='samplemodelforexport',
            name='file',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='SampleModelForTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(max_length=1)),
                ('batch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_app.HistoricRuns')),
            ],
        ),
    ]
