from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from .models import *
# Register your models here.


admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(ProductoImagen)