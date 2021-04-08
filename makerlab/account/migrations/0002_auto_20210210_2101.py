# Generated by Django 3.1.5 on 2021-02-10 21:01

from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='HT', help_text='Selectionner votre pays', max_length=2, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='Ex:john@winterfell.got', max_length=255, unique=True, verbose_name='Email '),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Ex:john', max_length=150, verbose_name='Prénom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Ex:snow', max_length=150, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Ex:+509XXXXXXXX', max_length=15, region=None, verbose_name='Téléphone'),
        ),
    ]