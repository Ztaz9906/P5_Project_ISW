# Generated by Django 4.1.3 on 2023-01-14 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Queseriademisinti', '0002_user_is_cliente_alter_compra_venta_pedido_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='pics'),
        ),
    ]
