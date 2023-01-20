from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import  authenticate, login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView 
import Queseriademisinti.forms as _forms
import Queseriademisinti.models as _models
import os
from django.contrib.auth.decorators import login_required, permission_required
from Queseriademisinti.decorador import for_client, for_repartidor_or_dependiente, for_admin, for_cliente_repartidor_or_dependiente,for_repartidor
from django.utils.decorators import method_decorator
User = get_user_model()

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="principal")
    elif request.user.is_cliente and request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="cliente")
    elif not request.user.is_cliente and request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="principal")

   
class ProductoClientListView(ListView):
        model = _models.Producto
        template_name = 'administrador.html'
        permission_required = 'Queseriademisinti.view_producto'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Listado de Productos'
            return context

def login_user(request):
    
    form = _forms.LoginForm(request.POST or None)

    if request.method == "GET":
        return render(request, 'sign-in/login.html', {'form': form})
    else:
        user = authenticate(
            request, email=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            if user.is_cliente:
                
                messages.success(request, "¡Usuario logueado correctamente!")
                return redirect('cliente')
            else:
                messages.success(request, "¡Usuario logueado correctamente!")
                return redirect('principal')
        else:
            messages.error(request, "¡Usuario o contraseña incorrectos!")
            return render(request, 'sign-in/login.html', {'form': form, "icon" : "error"})

############################ Registro Cliente ###################################
class RegisterView(SuccessMessageMixin,CreateView):
    model = _models.User
    template_name = "sign-in/register.html"
    form_class = _forms.RegisterClientForm
    success_url = reverse_lazy('login')
    success_message = "Usuario registrado"

############################ Gestionar Trabajador view ####################################
@method_decorator([for_admin,],name='dispatch') 
class TrabajadorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = _models.User
    template_name = 'pages/gest_trabajador/index.html'
    permission_required = 'Queseriademisinti.view_user'
    
    def get_context_data(self, **kwargs):
        is_cliente = False
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Trabajadores'
        context['object_list'] = User.objects.filter(is_cliente=is_cliente)
        return context

@method_decorator([for_admin],name='dispatch') 
class TrabajadorCreateDependienteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model =_models.User
    form_class = _forms.RegisterDependienteForm
    template_name = 'pages/gest_trabajador/add.html'
    success_url = reverse_lazy('trabajador')
    success_message = "Usuario Registrado"
    permission_required = 'Queseriademisinti.add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Dependiente'
        return context
@method_decorator([for_admin],name='dispatch')    
class TrabajadorCreateRepartidoView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model =_models.User
    form_class = _forms.RegisterRepartidorForm
    template_name = 'pages/gest_trabajador/add.html'
    success_url = reverse_lazy('trabajador')
    success_message = "Usuario Registrado"
    permission_required = 'Queseriademisinti.add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Repartidor'
        return context
@method_decorator([for_admin],name='dispatch')    
class TrabajadorCreateAdminView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model =_models.User
    form_class = _forms.RegisterAdminForm
    template_name = 'pages/gest_trabajador/add.html'
    success_url = reverse_lazy('trabajador')
    success_message = "Usuario Registrado"
    permission_required = 'Queseriademisinti.add_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Añadir Administrador'
        return context
@method_decorator([for_admin],name='dispatch') 
class TrabajadorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model =_models.User
    form_class =_forms.RegisterForm
    template_name = 'pages/gest_trabajador/edit.html'
    success_url = reverse_lazy('trabajador')
    success_message = "Usuario Editado"
    permission_required = 'Queseriademisinti.change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Trabajador'
        return context

@method_decorator([for_admin],name='dispatch') 
class TrabajadorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model =_models.User
    template_name = 'pages/gest_trabajador/delete.html'
    success_url = reverse_lazy('trabajador')
    success_message = "Usuario Eliminado"
    permission_required = 'Queseriademisinti.delete_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Trabajador'
        return context
################################# Gestionar Menu ###########################
@method_decorator([for_admin],name='dispatch') 
class ProductoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = _models.Producto
    template_name = 'pages/gest_producto/index.html'
    permission_required = 'Queseriademisinti.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        return context
@login_required
@permission_required('Queseriademisinti.add_producto', raise_exception=True)
@for_admin   
def createProducto (request):
    context = {}
    form = _forms.ProductoForm(request.POST or None, request.FILES)
    if form.is_valid():
            form.save()
            messages.success(request, "¡Producto añadido!")
            return redirect('producto')    
    context['form'] = form
    context['title'] = "Comprar"
    return render(request, 'pages/gest_producto/add.html', context)
    
@method_decorator([for_admin],name='dispatch')     
class ProductoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model =_models.Producto
    form_class =_forms.ProductoForm
    template_name = 'pages/gest_producto/edit.html'
    success_url = reverse_lazy('producto')
    success_message = "Producto Modificado"
    permission_required = 'Queseriademisinti.change_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'
        return context
    def updateimage(request, id):  #this function is called when update data
        old_image = _models.Producto.objects.get(id=id)
        form = _forms.ProductoForm(request.POST, request.FILES, instance=old_image)
        if form.is_valid():
            # deleting old uploaded image.
            image_path = old_image.foto.path
            if os.path.exists(image_path):
                os.remove(image_path)
            # the `form.save` will also update your newest image & path.
            form.save()
@method_decorator([for_admin],name='dispatch')            
class ProductoDelteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model =_models.Producto
    template_name = 'pages/gest_producto/delete.html'
    success_url = reverse_lazy('producto')
    success_message = "Producto eliminado"
    permission_required = 'Queseriademisinti.delete_producto'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Producto'
        return context
    
    def deleteimage(request, id):  #this function is called when update data
        old_image = _models.Producto.objects.get(id=id)
        form = _forms.ProductoForm(request.POST, request.FILES, instance=old_image)
        if form.is_valid():
            # deleting old uploaded image.
            image_path = old_image.foto.path
            if os.path.exists(image_path):
                os.remove(image_path)         

@login_required
@permission_required('Queseriademisinti.add_pedido', raise_exception=True)
@for_client    
def AddPedido(request, pk):
    print(request)
    context = {}
    form = _forms.PedidoForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            messages.error(request,'Usuario no autenticado')
            return redirect('add_pedido',pk) 
        if  not request.user.is_cliente:
            messages.error(request,'No tiene permiso para comprar')
            return redirect('add_pedido',pk) 
        p = _models.Producto.objects.get(pk=pk)
        if int(request.POST.get('cantidad')) < 0:
            messages.error(request,'Introdujo  una cantidad negativa')
        if p.cantidad - int(request.POST.get('cantidad')) <=0:
            messages.error(request,'Su compra excede la cantidad disponible')
        if int(request.POST.get('cantidad')) > 0 and p.cantidad - int(request.POST.get('cantidad')) >=0:
            p.cantidad -= int(request.POST.get('cantidad'))
            pedido = _models.Pedido(cantidad=int(request.POST.get('cantidad')), producto_id=_models.Producto.objects.get(pk=pk),
                                user_id=User.objects.get(pk=request.user.id))

            p.save() 
            pedido.save()
            messages.success(request, "¡Pedido añadido!")
            return redirect('cliente')
       
            
    context['forms'] = form
    context['title'] = "Comprar"
    context['object'] =_models.Producto.objects.get(pk=pk)
    return render(request, 'pages/pedido/add.html', context)

@login_required
@permission_required('Queseriademisinti.change_pedido', raise_exception=True)
@for_repartidor
def AddCompras(request, pk):
    print(request)
    context = {} 
    obj = _models.Pedido.objects.get(pk=pk)
    p = _models.Producto.objects.get(pk=obj.producto_id.id)
    form = _forms.PedidoUpdateForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        if obj.estado == 'En':
            compras = _models.Compra_venta(pedido_id=_models.Pedido.objects.get(pk=pk),user_id=User.objects.get(pk=obj.user_id.id),
                                           total_pagado = obj.cantidad * p.precio) 
            compras.save()
        messages.success(request, "¡Pedido Editado!")
        return redirect('pedido')
    context['pedido']  = _models.Pedido.objects.get(pk=pk)
    context['form'] = form
    return render(request, 'pages/pedido/edit.html', context) 
@method_decorator([for_repartidor_or_dependiente],name='dispatch')               
class PedidoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = _models.Pedido
    template_name = 'pages/pedido/index.html'
    permission_required = 'Queseriademisinti.view_pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        return context
@login_required
@permission_required('Queseriademisinti.view_pedido', raise_exception=True)
@for_client        
def list_cliente_buys(request):
    context = {}
    context['title'] = "Sus Pedidos"
    context['object_list'] = _models.Pedido.objects.filter(
        user_id=request.user)
    return render(request, 'pages/pedido/index_cliente.html', context)  
@method_decorator([for_cliente_repartidor_or_dependiente],name='dispatch') 
class PedidoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model =_models.Pedido
    template_name = 'pages/pedido/delete.html'
    success_message = "Pedido Eliminado"
    permission_required = 'Queseriademisinti.delete_pedido'
    def get_success_url(self):
        print(self.object.user_id.is_cliente)
        if self.object.user_id.is_cliente :
            return reverse('pedido_cliente')
        else:
            return reverse('pedido')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Pedido'
        return context
    
####### Listar Ventas o Compras #############
@method_decorator([for_admin],name='dispatch') 
class CompraVentaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
        model = _models.Compra_venta
        template_name = 'pages/compra_venta/index.html'
        permission_required = 'Queseriademisinti.view_compra_venta'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Listado de Pedidos'
            return context   
@login_required
@permission_required('Queseriademisinti.view_compras', raise_exception=True)
@for_client 
def list_Client_historial(request):
    context = {}
    context['title'] = "Sus Quejas"
    context['object_list'] = _models.Compra_venta.objects.filter(
        user_id=request.user)
    print(context["object_list"])
    return render(request, 'pages/compra_venta/index.html', context)       
########### Quejas ###########
@login_required
@permission_required('Queseriademisinti.view_quejas', raise_exception=True)
@for_client 
def list_Client_Queja(request):
    context = {}
    context['title'] = "Sus Quejas"
    context['object_list'] = _models.Quejas.objects.filter(
        usuario_id=request.user)
    print(context["object_list"])
    return render(request, 'pages/quejas/index.html', context)  
@method_decorator([for_admin],name='dispatch') 
class QuejasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView,):
        model = _models.Quejas
        template_name = 'pages/quejas/admin_index.html'
        permission_required = 'Queseriademisinti.view_quejas'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Listado de Pedidos'
            return context     
@login_required
@permission_required('Queseriademisinti.add_quejas', raise_exception=True)
@for_client       
def AddQueja(request):
    print(request)
    context = {}
    form = _forms.QuejaFrom(request.POST or None)
    if form.is_valid():
        quejas = _models.Quejas(titulo=request.POST.get('titulo'),tipo=request.POST.get('tipo'),descripcion=request.POST.get('descripcion'),
                                usuario_id=User.objects.get(pk=request.user.id))
        quejas.save()
        messages.success(request, "¡Queja añadida!")
        return redirect('quejas')

    context['form'] = form
    context['title'] = "Quejas"
    return render(request, 'pages/quejas/add.html', context)
@login_required
@permission_required('Queseriademisinti.view_quejas', raise_exception=True)
@for_client 
def list_Client_Queja_respuesta(request):
    context = {}
    context['title'] = "Sus Quejas"
    context['object_list'] = _models.Quejas.objects.filter(
        usuario_id=request.user)
    print(context["object_list"])
    return render(request, 'pages/quejas/index.html', context)  

############ Respuestas ###############################
@login_required
@permission_required('Queseriademisinti.view_respuestas', raise_exception=True)
@for_client
def list_Client_respuesta(request):
    context = {}
    context['title'] = "Respuestas a sus quejas o sugerencias"
    context['object_list'] = _models.Respuestas.objects.filter(
        usuario_id=request.user)
    print(context["object_list"])
    return render(request, 'pages/respuestas/user_index.html', context)  

class RespuestasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView,):
        model = _models.Respuestas
        template_name = 'pages/respuestas/index.html'
        permission_required = 'Queseriademisinti.view_respuestas'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Listado de Respuestas'
            return context     
@login_required
@permission_required('Queseriademisinti.add_respuestas', raise_exception=True)
@for_admin 
def AddRespuesta(request, pk):
    print(request)
    context = {}
    p = _models.Quejas.objects.get(pk=pk)
    form = _forms.RespuestaFrom(request.POST or None, instance = p)
    if form.is_valid():
        respuesta = _models.Respuestas(quejas_id=p,descripcion = request.POST.get('descripcion'),usuario_id=p.usuario_id) 
        respuesta.save()
        messages.success(request, "¡Respuesta añadida!")
        return redirect('respuesta')
    context['quejas'] = p
    context['form'] = form
    return render(request, 'pages/respuestas/add.html', context) 
@login_required
@permission_required('Queseriademisinti.change_respuestas', raise_exception=True)
@for_admin 
def RespuestaUpdateView(request, pk):
    print(request)
    context = {}
    obj = _models.Respuestas.objects.get(pk=pk)
    form = _forms.RespuestaFrom(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        messages.success(request, "¡Respuesta Editada!")
        return redirect('respuesta')
    context['quejas']  = _models.Respuestas.objects.get(pk=pk)
    context['form'] = form
    return render(request, 'pages/respuestas/edit.html', context)
@method_decorator([for_admin],name='dispatch') 
class RespuestaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model =_models.Respuestas
    template_name = 'pages/respuestas/delete.html'
    success_url = reverse_lazy('respuesta')
    success_message = "¡Respuesta Eliminada!"
    permission_required = 'Queseriademisinti.delete_respuesta'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Respuesta'
        return context
