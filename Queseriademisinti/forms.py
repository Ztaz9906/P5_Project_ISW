from django.contrib.auth.forms import AuthenticationForm
from django import forms
import Queseriademisinti.models as _
from django.contrib.auth.models import Group 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as T
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    error_messages = {
        'invalid_login': "Usuario o Contraseña incorrecto",
        'inactive': "Esta cuenta está inactiva.",
        'required': 'Este campo es requerido.',
    }
    

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

class RegisterClientForm(forms.ModelForm):
    
    password1 =forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    password2 =forms.CharField(label='Confirmar Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña nuevamente...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    class Meta:
        model = User
        fields = ['username','ci','tfno','dir','email','is_cliente']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'dir': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg '}),
            'is_cliente':forms.CheckboxInput(
                attrs={'checked' : 'True',
                       'disabled': 'True'}),
        } 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        if len(password1)<8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password2
    def clean_email(self):
        email = self.cleaned_data.get('email')
        a = User.objects.filter(email=email)
        if a.exists():
            raise forms.ValidationError("El correo ya existe")
        return email
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        a = User.objects.filter(ci=ci)
        if a.exists():
            raise forms.ValidationError("El Carnet de identidad ya existe")
        return ci
    def clean_tfno(self):
        tfno = self.cleaned_data.get('tfno')
        a = User.objects.filter(tfno=tfno)
        if a.exists():
            raise forms.ValidationError("Este telefono ya esta siendo utilizado")
        return tfno
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_cliente=True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        grupo = Group.objects.get(name='cliente')
        user.groups.add(grupo)
       
        return user


class RegisterForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ['username','ci','tfno','dir','email','groups','password']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'dir': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg '
                       }),
            'groups' : forms.CheckboxSelectMultiple(),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-lg '})
        } 
        error_messages = {
            'email': {
                'required': "Este campo es requerido.",
                'unique': "El correo ya existe"
            },
            'ci': {
                'required': "Este campo es requerido.",
                'unique': "El Carnet de identidad ya existe"
            },
            'tfno': {
                'required': "Este campo es requerido.",
                'unique': "Este telefono ya esta siendo utilizado"
            }   
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        user.groups.clear()
        for g in self.cleaned_data['groups'] :
                user.groups.add(g)
        return user

class RegisterDependienteForm(forms.ModelForm):
   
    password1 =forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    password2 =forms.CharField(label='Confirmar Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña nuevamente...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    class Meta:
        model = User
        fields = ['username','ci','tfno','dir','email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'dir': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg '}),
           
        } 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        if len(password1)<8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password2
    def clean_email(self):
        email = self.cleaned_data.get('email')
        a = User.objects.filter(email=email)
        if a.exists():
            raise forms.ValidationError("El correo ya existe")
        return email
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        a = User.objects.filter(ci=ci)
        if a.exists():
            raise forms.ValidationError("El Carnet de identidad ya existe")
        return ci
    def clean_tfno(self):
        tfno = self.cleaned_data.get('tfno')
        a = User.objects.filter(tfno=tfno)
        if a.exists():
            raise forms.ValidationError("Este telefono ya esta siendo utilizado")
        return tfno
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        grupo = Group.objects.get(name='dependiente')
        user.groups.add(grupo)
        return user
    
class RegisterRepartidorForm(forms.ModelForm):
   
    password1 =forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    password2 =forms.CharField(label='Confirmar Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña nuevamente...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    class Meta:
        model = User
        fields = ['username','ci','tfno','dir','email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'dir': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg '}),
           
        } 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        if len(password1)<8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password2
    def clean_email(self):
        email = self.cleaned_data.get('email')
        a = User.objects.filter(email=email)
        if a.exists():
            raise forms.ValidationError("El correo ya existe")
        return email
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        a = User.objects.filter(ci=ci)
        if a.exists():
            raise forms.ValidationError("El Carnet de identidad ya existe")
        return ci
    def clean_tfno(self):
        tfno = self.cleaned_data.get('tfno')
        a = User.objects.filter(tfno=tfno)
        if a.exists():
            raise forms.ValidationError("Este telefono ya esta siendo utilizado")
        return tfno
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        grupo = Group.objects.get(name='repartidor')
        user.groups.add(grupo)
        return user
    
class RegisterAdminForm(forms.ModelForm):
   
    password1 =forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
             'requiered': 'requiered',
        }
     ))
    password2 =forms.CharField(label='Confirmar Contraseña', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña nuevamente...',
            'id': 'password1',
            'requiered': 'requiered',
        }
     ))
    class Meta:
        model = User
        fields = ['username','ci','tfno','dir','email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'dir': forms.TextInput(
                attrs={'class': 'form-control form-control-lg '}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg '}),
            
        } 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2 :
            raise forms.ValidationError('Las contraseñas no coinciden')
        if len(password1)<8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password2
    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        a = User.objects.filter(email=email)
        if a.exists():
            raise forms.ValidationError("El correo ya existe")
        return email
    def clean_ci(self):
        ci = self.cleaned_data.get('ci')
        a = User.objects.filter(ci=ci)
        if a.exists():
            raise forms.ValidationError("El Carnet de identidad ya existe")
        return ci
    def clean_tfno(self):
        tfno = self.cleaned_data.get('tfno')
        a = User.objects.filter(tfno=tfno)
        if a.exists():
            raise forms.ValidationError("Este telefono ya esta siendo utilizado")
        return tfno
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        grupo = Group.objects.get(name='admin')
        user.groups.add(grupo)
        return user  
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = _.Producto
        fields = ['nombre','cantidad','precio','foto']
        error_messages = {
            'nombre': {
                'required': "Completa este campo.",
                'unique': "El producto ya existe"
            },
            'cantidad': {
                'required': "Completa este campo.",
                
            },
            'precio': {
                'required': "Completa este campo.",
            }   
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        a = _.Producto.objects.filter(nombre=nombre)
        if a.exists():
            raise forms.ValidationError("El nombre del Producto ya existe")
        return nombre  
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <0:
            raise forms.ValidationError("La cantidad no puede ser negativa")
        return cantidad
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <0:
            raise forms.ValidationError("El precio no puede ser negativo")
        return precio

class PedidoForm(forms.ModelForm):
    class Meta:
        model = _.Pedido
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control form-control-lg '})
        }
        
        
class PedidoUpdateForm(forms.ModelForm):
    class Meta:
        model = _.Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control form-control-lg '})
        }
    
class CompraVentaForm (forms.ModelForm):
    class Meta:
        model =_.Compra_venta
        fields = ('__all__')

class QuejaFrom(forms.ModelForm):
    class Meta :
        model =_.Quejas
        fields = ['titulo','descripcion','tipo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control form-control-lg '}),
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-lg '}),
            'descripcion' : forms.Textarea(attrs={'class': 'form-control form-control-lg '})
        }
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        a = _.Quejas.objects.filter(titulo=titulo)
        if a.exists():
            raise forms.ValidationError("El título ya existe")
        return titulo
    
       
class RespuestaFrom(forms.ModelForm):
    class Meta :
        model =_.Quejas
        fields = ['descripcion']
        widgets = {
            'descripcion' : forms.Textarea(attrs={'class': 'form-control form-control-lg '})
        }
