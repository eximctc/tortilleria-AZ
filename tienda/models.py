from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
