# Generated by Django 5.2.3 on 2025-07-01 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0003_rename_atleta_encomendaequipamentos_atleta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encomendaequipamentos',
            name='equipamento',
        ),
        migrations.AddField(
            model_name='encomendaequipamentos',
            name='equipamento',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='equipamentos.equipamentos'),
            preserve_default=False,
        ),
    ]
