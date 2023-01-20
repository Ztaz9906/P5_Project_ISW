from django.contrib import admin
import Queseriademisinti.models as M

# images
class ProductAdmin(admin.ModelAdmin): # new
     list_display = ['nombre','img_tag']

# Register your models here.
admin.site.register(M.User)
admin.site.register(M.Producto,ProductAdmin)
admin.site.register(M.Quejas)
admin.site.register(M.Respuestas)
admin.site.register(M.Pedido)
admin.site.register(M.Compra_venta)

