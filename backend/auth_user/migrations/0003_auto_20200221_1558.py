# Generated by Django 3.0.2 on 2020-02-21 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0002_jobposition_office_subdivision_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobposition',
            options={'ordering': ['name'], 'verbose_name': 'Должность', 'verbose_name_plural': 'Должности'},
        ),
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['name'], 'verbose_name': 'Офис', 'verbose_name_plural': 'Офисы'},
        ),
        migrations.AlterModelOptions(
            name='subdivision',
            options={'ordering': ['name'], 'verbose_name': 'Подразделение', 'verbose_name_plural': 'Подразделения'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='job_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_user.JobPosition', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_user.Office', verbose_name='Офис'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='subdivision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth_user.Subdivision', verbose_name='Подразделение'),
        ),
    ]