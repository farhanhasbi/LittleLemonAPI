from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Category'

    def __str__(self):
        return f'{self.pk}. {self.title}'


class MenuItem(models.Model):
   title = models.CharField(max_length=255, db_index=True)
   price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
   feature = models.BooleanField(db_index=True)
   category = models.ForeignKey(Category, on_delete=models.CASCADE)

   class Meta:
    verbose_name = 'Menu item'
    ordering = ['pk']

   def __str__(self):
       return f'{self.pk}.{self.title} - {self.price}'
        

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['pk']
        unique_together = ('menuitem', 'user')

    def __str__(self):
        return f'{self.pk}. {self.user} - Menu: {self.menuitem.title} - Quantity: {self.quantity} - Total: {self.price}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='Delivery_crew', null=True)
    status = models.BooleanField(db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(db_index=True, blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.pk}. {self.user} - Total: {self.total}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_Items')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return f'{self.pk}. {self.order.user} - Menu: {self.menuitem.title} - Quantity: {self.quantity} - Total: {self.price}'

    class Meta:
        ordering = ['pk']
        unique_together = ('order', 'menuitem')

