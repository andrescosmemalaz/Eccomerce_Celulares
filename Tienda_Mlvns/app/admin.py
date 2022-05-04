from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import(
    Costumer,
    Product,
    Carrito,
    PedidoRealizado,
)

@admin.register(Costumer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price',
                    'description','brand', 'category','product_image']

@admin.register(Carrito)
class CarritoModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(PedidoRealizado)
class PedidoRealizadoAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status']

# def customer_info(self, obj):
#   link = reverse("admin:app_costumer_change", args=[obj.costumer.pk])
#   return format_html('<a href="{}">{}</a>', link, obj.costumer.name)
# # Register your models here.

