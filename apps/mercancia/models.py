from django.db import models

# Create your models here.



class Pedido(models.Model):
    choice_estado = (
        ("R", "En camino"),
        ("L", "Listo"),
        ("D", "Demorado"),
    )
    numero_pedido = models.IntegerField()
    detalle = models.CharField(max_length=30, blank=True)
    # estado is a string choice, so use CharField
    estado = models.CharField(max_length=1, choices=choice_estado)
    metodo_pago = models.CharField(max_length=30, blank=True)  # revisit payment method

    
    def __str__(self):
        return f"Pedido {self.numero_pedido} – {self.get_estado_display()}"

    class Meta:
        ordering = ['numero_pedido']
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

class Producto(models.Model):
    # choices must be an iterable of 2-tuples, not a dict
    choice_categoria = (
        ("P", "Pullover"),
        ("J", "Jarra"),
    )
    choice_tipo = (
        ("Per", "Personalizado"),
        ("E", "Estandar"),
    )

    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()  # IntegerField does not accept max_length
    categoria = models.CharField(max_length=5, choices=choice_categoria)
    tipo = models.CharField(max_length=5, choices=choice_tipo)
    descripcion = models.TextField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)
    pedido_id = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
    
class ProductoImagen(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="imagenes"
    )

    imagen = models.ImageField(upload_to="productos/")

    """ def __str__(self):
        return self.nombre"""

class Usuario(models.Model): 
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    correo = models.CharField(max_length=30,blank=True)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=30)
    
    
    