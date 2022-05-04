from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

STATE_CHOICES = (
    ('Lima','Lima'),
    ('Amazonas','Amazonas'),
    ('Ancash','Ancash'),
    ('Apurimac','Apurimac'),
    ('Arequipa','Arequipa'),
    ('Ayacucho','Ayacucho'),
    ('Cajamarca','Cajamarca'),
    ('Callao','Callao'),
    ('Cusco','Cusco'),
    ('Huancavelica','Huancavelica'),
    ('Huanuco','Huanuco'),
    ('Ica','Ica'),
    ('Junín','Junín'),
    ('La Libertad','La Libertad'),
    ('Lambayeque','Lambayeque'),
    ('Loreto','Loreto'),
    ('Madre de Dios','Madre de Dios'),
    ('Moquegua','Moquegua'),
    ('Pasco','Pasco'),
    ('Piura','Piura'),
    ('Puno','Puno'),
    ('San Martín','San Martín'),
    ('Tacna','Tacna'),
    ('Tumbes','Tumbes'),
    ('Ucayali','Ucayali')
)


class  Costumer(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 name = models.CharField(max_length=200)
 locality = models.CharField(max_length=200)
 city = models.CharField(max_length=50)
 zipcode = models.IntegerField()
 state = models.CharField(choices=STATE_CHOICES, max_length=50)
 
 def __str__(self):
     return str(self.id)


CATEGORY_CHOICES = (
    ('C', 'Celulares'),
    ('L', 'Laptops'),
    ('T', 'Tablets'),
    ('G','Games'),
    ('PC',' PC de Escritorio'),
    ('F','Fundas para Celulares'),
    ('M','Micas Protectoras'),
    ('A','Audifonos'),
    ('T','Tarjetas de memoria'),
    ('B','Baterias, Cargadores y Otros'),
    ('R', 'Repuestos de Celulares')
)


class Product(models.Model):
 title = models.CharField(max_length=100)
 selling_price = models.FloatField()
 discounted_price = models.FloatField()
 description = models.TextField()
 brand = models.CharField(max_length=100)
 category = models.CharField(choices= CATEGORY_CHOICES,
 max_length=2)
 product_image = models.ImageField(upload_to='productimg')
    
 def __str__(self):
    return str(self.id)

 @property
 def costo_total(self):
   return self.quantity * self.prduct.selling_price


class Carrito(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.PositiveBigIntegerField(default=1)

 def __str__(self):
  return str(self.id)

 @property
 def costo_total(self):
   return self.quantity * self.product.selling_price


STATUS_CHOICES = (
    ('Aceptado','Aceptado'),
    ('Envasado','Envasado'),
    ('En camino','En camino'),
    ('Entregado','Entregado'),
    ('Cancelar','Cancelar')
)

class PedidoRealizado(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 customer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.PositiveBigIntegerField(default=1)
 ordered_date = models.DateTimeField(auto_now_add=True)
 status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending') 
 

 @property
 def costo_total(self):
   return self.quantity * self.product.selling_price
