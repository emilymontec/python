from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que_paso', models.TextField()),
                ('gravedad', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('critica', 'Crítica')], max_length=10)),
                ('como_se_arreglo', models.TextField(blank=True)),
                ('estado', models.CharField(choices=[('abierto', 'Abierto'), ('en_progreso', 'En progreso'), ('cerrado', 'Cerrado')], default='abierto', max_length=15)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidentes', to='App.proyecto')),
            ],
        ),
    ]

