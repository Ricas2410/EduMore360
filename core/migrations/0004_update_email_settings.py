from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_systemconfiguration_smtp_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemconfiguration',
            name='smtp_username',
            field=models.CharField(default='edumore@colaname.com', max_length=100),
        ),
        migrations.AlterField(
            model_name='systemconfiguration',
            name='smtp_password',
            field=models.CharField(default='sipv ehpg wtbw kesc', max_length=100),
        ),
        migrations.AlterField(
            model_name='systemconfiguration',
            name='default_from_email',
            field=models.EmailField(default='edumore@colaname.com', max_length=254),
        ),
    ]
