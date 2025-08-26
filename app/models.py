from django.db import models

# Create Category model.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str___(self):
        return f"Category Name : {self.name}."
    
# create a tag model.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Tag Name : {self.name}."
    

    
# Create product model.
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    crerated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def __str__(self):
        return f"Product Name : {self.name}, Category : {self.category.name}, Price : {self.price}, Stock : {self.stock}."

# Create customer model.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Customer Name : {self.first_name} {self.last_name}, Email : {self.email}."
    



