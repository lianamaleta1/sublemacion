from django.db import models

# Create your models here.
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
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    choice_estado = (
        ("R", "En camino"),
        ("L", "Listo"),
        ("D", "Demorado"),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=30, blank=True)
    # estado is a string choice, so use CharField
    estado = models.CharField(max_length=1, choices=choice_estado)
    metodo_pago = models.CharField(max_length=30, blank=True)  # revisit payment method


class Usuario(models.Model): 
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    correo = models.CharField(max_length=30,blank=True)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=30)
    metodo_pago = models.CharField(max_length=30, blank=True)
    
    