Pasos para correr el proyecto:

1- Crear el virtual env con el comando python -m venv .env

2- Activar el virtual env creado con el comando .env\Scripts\activate

3- Instalar las dependencias con el comando pip install django

4- Hacer la migracion de las tablas de la BD para crear la misma: python manage.py makemigrations

5- Migrar la base de datos: python manage.py migrate

6- Crear un superusuario: python manage.py createsuperuser

7- Correr el servidor y abrir la pagina de inicio del mismo: python manage.py runserver