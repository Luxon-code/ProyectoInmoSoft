<<<<<<< HEAD
# Generated by Django 4.2 on 2023-10-06 22:31
=======
# Generated by Django 4.2.2 on 2023-10-06 22:54
>>>>>>> ae94ec5af6a17c15140db9684ec53183b412fd6f

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userCedula', models.CharField(db_comment='Numero de cedula del usuario', error_messages={'unique': 'Ya existe un usuario con esta cedula'}, max_length=20, unique=True)),
                ('userTelefono', models.CharField(db_comment='Numero de telefono del usuario', max_length=20)),
                ('userFoto', models.FileField(blank=True, db_comment='Foto del Usuario', null=True, upload_to='fotos/')),
                ('userTipo', models.CharField(choices=[('Administrador', 'Administrador'), ('Asesor', 'Asesor')], db_comment='Nombre Tipo de usuario', max_length=15)),
                ('username', models.CharField(error_messages={'unique': 'Ya existe un usuario con ese nombre de usuario'}, max_length=150, unique=True, verbose_name='username')),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'Ya existe un usuario con ese correo electronico'}, max_length=254, unique=True, verbose_name='email address')),
                ('userfechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('userfechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Apartamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apaNumeroHabitaciones', models.IntegerField(db_comment='Numero de habitaciones de un inmueble')),
                ('apaAreaConstruida', models.CharField(db_comment='Area construida del inmueble', max_length=20)),
                ('apaCategoria', models.CharField(choices=[('Tipo A', 'Tipo A'), ('Tipo B', 'Tipo B'), ('Tipo C', 'Tipo C'), ('Tipo penthouse', 'Tipo penthouse')], db_comment='Tipo de apartamento', max_length=15)),
                ('apaPrecioVivienda', models.BigIntegerField(db_comment='Precio de vivienda')),
                ('apafechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('apafechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Casas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casNumeroHabitaciones', models.IntegerField(db_comment='Numero de habitaciones de un inmueble')),
                ('casAreaConstruida', models.CharField(db_comment='Area construida del inmueble', max_length=20)),
                ('casCategoria', models.CharField(choices=[('Tipo A', 'Tipo A'), ('Tipo B', 'Tipo B'), ('Tipo C', 'Tipo C')], db_comment='Tipo de casa', max_length=15)),
                ('casPrecioVivienda', models.BigIntegerField(db_comment='Precio de vivienda')),
                ('casfechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('casfechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliNombre', models.CharField(db_comment='Nombre del cliente', max_length=50)),
                ('cliApellido', models.CharField(db_comment='Apellido del cliente', max_length=50)),
                ('cliTelefono', models.CharField(db_comment='Telefono del cliente', max_length=50)),
                ('cliCorreo', models.CharField(db_comment='Correo del cliente', max_length=50)),
                ('cliCedula', models.CharField(db_comment='cedula del cliente', max_length=50)),
                ('cliDireccion', models.CharField(db_comment='Direccion del cliente', max_length=50)),
                ('cliEstadoCivil', models.CharField(choices=[('Soltero', 'Soltero'), ('Casado', 'Casado')], db_comment='Estado Civil del cliente', max_length=50)),
                ('clifechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('clifechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Familiar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faNombre', models.CharField(db_comment='Nombre del familiar', max_length=50)),
                ('faApellido', models.CharField(db_comment='Apellido del familiar', max_length=50)),
                ('faTelefono', models.CharField(db_comment='Telefono del familiar', max_length=50)),
                ('faCorreo', models.CharField(db_comment='Correo del familiar', max_length=50)),
                ('faCedula', models.CharField(db_comment='cedula del familiar', max_length=50)),
                ('faDireccion', models.CharField(db_comment='Direccion del familiar', max_length=50)),
                ('fafechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fafechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inmEntregaDeObra', models.CharField(choices=[('Obra Gris', 'Obra Gris'), ('Obra Blanca', 'Obra Blanca'), ('Obra Full acabado', 'Obra Full acabado')], db_comment='Entrega del inmueble', max_length=20)),
                ('inmEstado', models.CharField(choices=[('Disponible', 'Disponible'), ('Separado', 'Separado'), ('Vendido', 'Vendido')], db_comment='estado de disponibilidad del Inmueble', max_length=20)),
                ('inmfechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('inmfechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('inmApartamento', models.ForeignKey(db_comment='hace refencia al tipo de inmueble', null=True, on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.apartamento')),
                ('inmCasa', models.ForeignKey(db_comment='hace referencia al tipo de inmueble', null=True, on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.casas')),
            ],
        ),
        migrations.CreateModel(
            name='PlanDePago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plaFechaInicial', models.DateField(db_comment='Fecha de inicio del plan de pago')),
                ('plaFechaFinal', models.DateField(db_comment='Fecha de final del plan de pago')),
                ('plaNumCuota', models.IntegerField(db_comment='Numero de cuotas')),
                ('plaCuotaInicial', models.BigIntegerField(db_comment='Valor de la cuota Inicial')),
                ('plaValorDeCuota', models.BigIntegerField(db_comment='Valor de la Cuota')),
                ('plafechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora de registro')),
                ('plafechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubiDepartamento', models.CharField(db_comment='ubicacion del departamento del proyecto', max_length=255)),
                ('ubiCuidad', models.CharField(db_comment='ubicacion de la cuidad del prouceto', max_length=255)),
                ('ubiDireccion', models.CharField(db_comment='Direccion del proyecto', max_length=255)),
                ('ubifechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('ubifechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venFechaSeparacion', models.DateField(db_comment='Fecha Separacion del cliente')),
                ('venFechaCreacion', models.DateField(auto_now=True, db_comment='Fecha de creacion')),
                ('venfechaModificacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('venEstadoMora', models.BooleanField(db_comment='Estado de mora', default=False)),
                ('venCliente', models.ForeignKey(db_column='Cliente interesado en el inmueble', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.cliente')),
                ('venInmueble', models.ForeignKey(db_comment='Inmueble disponible para la venta', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.inmueble')),
                ('venUsuario', models.ForeignKey(db_comment='Asesor', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regFechaPago', models.DateField(auto_now=True, db_comment='Fecha de pago')),
                ('regValorPago', models.BigIntegerField(db_comment='Valor de pago de la cuota')),
                ('regPendiente', models.BigIntegerField(db_comment='Valor pendiente')),
                ('regNumCuota', models.BigIntegerField(db_comment='Número de cuota')),
                ('regRecaudo', models.BigIntegerField(db_comment='Recaudo total')),
                ('regfechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('regfechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('regFoto', models.FileField(blank=True, db_comment='', null=True, upload_to='fotosReg/')),
                ('regPlanDePago', models.ForeignKey(db_comment='plan de pago', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.plandepago')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proNombre', models.CharField(db_comment='Nombre del proyecto', max_length=25)),
                ('proDescripcion', models.TextField(db_comment='Descripcion del proyecto', max_length=255)),
                ('proTipo', models.CharField(choices=[('VIS', 'VIS'), ('VIP', 'VIP'), ('NO VIS', 'NO VIS')], db_comment='Tipo de proyecto', default='VIS', max_length=255)),
                ('proFiducia', models.CharField(choices=[('Bancolombia', 'Bancolombia'), ('BBVA', 'BBVA'), ('Banco de Bogota', 'Banco de Bogota'), ('Banco Caja Social', 'Banco Caja Social'), ('Grupo Bancolombia', 'Grupo Bancolombia'), ('Davivienda', 'Davivienda'), ('Banco de Occidente', 'Banco de Occidente')], db_comment='Fiducia que va a contriduir en el proyecto', max_length=25)),
                ('proFoto', models.FileField(blank=True, db_comment='Foto del Proyecto', null=True, upload_to='fotosPro/')),
                ('proNumeroManzanasTorres', models.IntegerField(db_comment='Numero de manzanas o torres')),
                ('proCostoSeparacion', models.BigIntegerField(db_comment='Costo de separacion del inmuble')),
                ('proEstado', models.BooleanField(db_comment='Estado', default=True)),
                ('proNumeroInmuebles', models.IntegerField(db_comment='Numero de inmueble por manzanas o torres')),
                ('proNumeroDePisos', models.IntegerField(db_comment='Numero de pisos')),
                ('proTotalInmuebles', models.IntegerField(db_comment='Total de inmuebles en todo el proyecto')),
                ('proParqueadero', models.CharField(choices=[('Comunal', 'Comunal'), ('Asignado', 'Asignado'), ('Propio', 'Propio')], db_comment='Tipo de parqueadero que tiene el proyecto', max_length=25)),
                ('proCantidadParqueadero', models.BigIntegerField(db_comment='Cantidad de parqueaderos que tendra el proyecto')),
                ('profechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('profechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('proUbicacion', models.ForeignKey(db_comment='Ubicacion del proyecto', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.ubicacion')),
            ],
        ),
        migrations.AddField(
            model_name='plandepago',
            name='plaVenta',
            field=models.ForeignKey(db_comment='venta', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.venta'),
        ),
        migrations.AddField(
            model_name='inmueble',
            name='inmProyecto',
            field=models.ForeignKey(db_comment='proyecto al que corresponde el inmueble', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.proyecto'),
        ),
        migrations.CreateModel(
            name='fotoInmuble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fotInmuble', models.FileField(blank=True, db_comment='Fotos del Imueble', null=True, upload_to='fotosInm/')),
                ('fotfechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fotfechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('fotProyecto', models.ForeignKey(db_comment='llave foranea para defenir a que proyecto pertenece la foto del inmuble', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='ClienteInteresado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliNombre', models.CharField(db_comment='Nombre del cliente', max_length=50)),
                ('cliApellido', models.CharField(db_comment='Apellido del cliente', max_length=50)),
                ('cliTelefono', models.CharField(db_comment='Telefono del cliente', max_length=50)),
                ('cliCorreo', models.CharField(db_comment='Correo del cliente', max_length=50)),
                ('cliCedula', models.CharField(db_comment='cedula del cliente', max_length=50)),
                ('clifechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('clifechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('cliProyecto', models.ForeignKey(db_comment='Proyecto interesado del cliente', on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.proyecto')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='cliFamiliar',
            field=models.ForeignKey(db_comment='Familiar del cliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='appInmoSoft.familiar'),
        ),
    ]
