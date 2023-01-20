from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as T
from django.utils.html import mark_safe
from PIL import Image as Im
from django.core.validators import RegexValidator
validate_ci = RegexValidator('^\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{5}$', 'Carnet invalido')
validate_tfno = RegexValidator('^\+53\d{8}$', 'Teléfono invalido')
validate_name = RegexValidator('^[A-Za-záãäéëêíîóöúüñç\s]*$', 'Solo Letras,Introduzca Nombre y dos apellidos')
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,username,dir,ci,tfno,password=None,**extra_kwargs):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')
        
        user = self.model(email=self.normalize_email(email), 
                          username=username,
                          dir=dir, 
                          ci=ci, 
                          tfno=tfno,
                          **extra_kwargs                
        )
        user.is_cliente=True
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,username,dir,ci,tfno,password,**extra_kwargs):
        user = self.create_user(email,
                                username=username,
                                dir=dir, 
                                ci=ci, 
                                tfno=tfno,
                                password=password,
                                **extra_kwargs
        )
        user.is_cliente=False
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, default="Cambio",validators=[validate_name])
    dir = models.CharField(max_length=255,blank=False, null=False)
    ci = models.CharField(max_length=11, unique=True, null=False, blank=False,validators=[validate_ci])
    tfno = models.CharField(max_length=50,validators=[validate_tfno],unique=True)
    is_cliente = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'dir', 'ci', 'tfno']

    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def if_staf(self):
        return self.is_staff
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True, null=False, blank=False)
    foto = models.ImageField(upload_to='pics',null=True, blank=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Precio',blank=False, null=False)
    cantidad = models.IntegerField(blank=False, null=False)
   
    class Meta:
        ordering = ['nombre']
    # para ver en adminDjango
    def img_tag(self): #new
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.foto))
    def save(self): # new
        super().save()
        img = Im.open(self.foto.path)
        # resize it
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.foto.path)
        
    def __str__(self):
        """Return String"""
        return self.nombre

class Quejas(models.Model):
    
    class tipoqueja (models.TextChoices):
        queja= 'Q', T('Queja')
        sugerencia= 'S', T('Sugerencia')
        
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=tipoqueja.choices, null=False, blank=False)
    titulo = models.CharField(max_length=255, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    fecha_creacion = models.DateField(blank=False, null=False, auto_now=True)

    class Meta:
        ordering = ['fecha_creacion','tipo', 'titulo']

    def __str__(self):
        return "%s %s" % (self.tipo, self.titulo)

class Respuestas(models.Model):
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quejas_id = models.ForeignKey(Quejas,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    fecha_creacion = models.DateField(blank=False, null=False, auto_now=True)
    
    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return "%s" % (self.fecha_creacion)

class estadocoices (models.TextChoices):
        espera= 'E', T('Espera')
        aceptado= 'A', T('Aceptado')
        entregado = 'En', T('Entregado')
        
class Pedido(models.Model):
      
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto,on_delete=models.CASCADE)
    estado = models.CharField(max_length=2, choices=estadocoices.choices, null=False, blank=False, default='E')
    cantidad = models.IntegerField(blank=False, null=False)
    class Meta:
        ordering = ['estado']
    
    def __str__(self):
        """Return String"""
        return self.estado
     
class Compra_venta(models.Model):
    pedido_id = models.ForeignKey(Pedido,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    total_pagado = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total',blank=False, null=False)
    fecha_creacion = models.DateField(blank=False, null=False, auto_now=True)
    
    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return "%s" % (self.fecha_creacion)
