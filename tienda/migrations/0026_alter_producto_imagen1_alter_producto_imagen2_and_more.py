# Generated by Django 5.1.4 on 2025-01-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0025_alter_usuario_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen1',
            field=models.ImageField(blank=True, default='uploads/default_P.png', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen2',
            field=models.ImageField(blank=True, default='uploads/default_P.png', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen3',
            field=models.ImageField(blank=True, default='uploads/default_P.png', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen4',
            field=models.ImageField(blank=True, default='uploads/default_P.png', null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen5',
            field=models.ImageField(blank=True, default='uploads/default_P.png', null=True, upload_to='uploads/'),
        ),
    ]
