from django.urls import path
from django.contrib.auth.views import LogoutView
from Queseriademisinti import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('principal/',views.ProductoClientListView.as_view(), name='principal'),
    #### Menu #####
    path('menu/',views.ProductoClientListView.as_view(), name='cliente'),
    #### Compra_venta ########
     path('Historial/',views.CompraVentaListView.as_view(), name='historial'),
     path('Su_Historial/',views.list_Client_historial, name='cliente_historial'),
    ####### Quejas #########
    path('Quejas_y_sugerencias/',views.list_Client_Queja, name='quejas'),
    path('administrador/Quejas_y_sugerencias/',views.QuejasListView.as_view(), name='admin_quejas'),
    path('Quejas/add/',views.AddQueja, name='add_queja'),
    ######## Respuestas #########
    path('respuestas/',views.RespuestasListView.as_view(), name='respuesta'),
    path('tus_respuestas/',views.list_Client_respuesta, name='user_respuesta'),
    path('respuestas/add/<int:pk>/',views.AddRespuesta, name='add_repuesta'),
    path('respuestas/edit/<int:pk>/',views.RespuestaUpdateView, name='edit_repuesta'),
    path('respuestas/delete/<int:pk>/',views.RespuestaDeleteView.as_view(), name='eliminar_respuesta'),
    ### Pedido #####
    path('pedidos/edit/<int:pk>/',views.AddCompras, name='edit_pedido'),
    path('pedidos/',views.PedidoListView.as_view(), name='pedido'),
    path('pedidos_cliente/',views.list_cliente_buys, name='pedido_cliente'),
    path('pedidos/add/<int:pk>/',views.AddPedido, name='add_pedido'),
    path('pedidos/delete/<int:pk>/',views.PedidoDeleteView.as_view(), name='eliminar_pedido'),
    ############# Gestionar Trabajador###########
    path('trabajador/',views.TrabajadorListView.as_view(),name='trabajador'),
    path('trabajador/addAdmin/',views.TrabajadorCreateAdminView.as_view(),name='add_admin'),
    path('trabajador/addDependiente/',views.TrabajadorCreateDependienteView.as_view(),name='add_dependiente'),
    path('trabajador/addRepartidor/',views.TrabajadorCreateRepartidoView.as_view(),name='add_repartidor'),
    path('trabajador/edit/<int:pk>/',views.TrabajadorUpdateView.as_view(),name='editar_trabajador'),
    path('trabajador/delete/<int:pk>/',views.TrabajadorDeleteView.as_view(), name='eliminar_trabajador'),
    ############# Gestionar producto #############
    path('producto/',views.ProductoListView.as_view(),name='producto'),
    path('producto/add/',views.createProducto,name='add_producto'),
    path('producto/edit/<int:pk>/',views.ProductoUpdateView.as_view(),name='editar_producto'),
    path('producto/delete/<int:pk>/',views.ProductoDelteView.as_view(), name='eliminar_producto'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)