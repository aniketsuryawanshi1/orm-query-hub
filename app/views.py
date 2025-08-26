from .models import Category, Product, Customer


# Creating a object in the database

# ****************************Creating a single object in the database****************************
# Creating a new category.
electornics = Category.objects.create(name='Electronics')

# Creating a new product.
Laptop = Product.objects.create(
    name='Laptop',
    category = electornics,
    price = 1000.00,
    stock = 50
)

# Creating a new customer.
customer1 = Customer.objects.create(
    first_name = 'Aniket',
    last_name = 'Suryavanshi',
    email = 'aniketsuryavanshi309@gmail.com',
)


# *************************************** End *******************************************


# ****************************Creating bulk objects in the database****************************

# Creating multiple categories.
categories = [
    Category(name='Books'),
    Category(name='Clothing'),
    Category(name='Sports'),
    Category(name='Toys'),
    Category(name='Furniture'),
    
]

created_categories = Category.objects.bulk_create(categories)

# creating a multiple products.
product_list = [
    Product(name='Book1', category=created_categories[0], price=15.99, stock=100),
    Product(name='Shirt', category=created_categories[1], price=29.99, stock=50),
    Product(name='Football', category=created_categories[2], price=19.99, stock=75),
    Product(name='Doll', category=created_categories[3], price=9.99, stock=200),
    Product(name='Sofa', category=created_categories[4], price=499.99, stock=10),
]

create_products = Product.objects.bulk_create(product_list)

# creating multiple customers.
customers = [
    Customer(first_name='John', last_name='Doe', email='testuser123@gmail.com'),
    Customer(first_name='Jane', last_name='Smith', email='testuser456@gmail.com'),
    Customer(first_name='Alice', last_name='Johnson', email='testuser987@gmail.com'),
]


create_customers = Customer.objects.bulk_create(customers)

# *************************************** End *******************************************`


# Reading Objects (all, filter, get, exclude, order_by)


# Get all objects from category model.

all_categories = Category.objects.all()

# get count of all objects in category model.
categories_count = Category.objects.count()

# Get all objects from product model.
all_products = Product.objects.all()

# Get all objects from customer model.
all_customers = Customer.objects.all()

# Get specific object from category model.
specific_category = Category.objects.get(id=1)

# get spefic object from product model.
spefic_product = Product.objects.get(id=1)

# Get specific object from customer model.
specific_customer = Customer.objects.get(id=1)

# **************************filtering objects********************************

# Get all products in a specific category.
products_in_category = Product.objects.filter(category='Books')

# Get all customers with a specific first name.
customers_with_first_name = Customer.objects.filter(first_name='John')

# Get all products with a price greater than a specific value. (gt - greater than)
products_with_price_greater_than = Product.objects.filter(price__gt=20.00)

# Get all products with a price less than a specific value. (lt - less than)
products_with_price_less_than = Product.objects.filter(price__lt=100.00)


# Get all products with a specific stock value.
products_with_specific_stock = Product.objects.filter(stock=50)

# Get alll products with a specific stock value and category.
in_stock_electronics = Product.objects.filter(
    category__name='Electronics',
    stock__gt=0
)

# ***************************Get specific objects********************************
# Get a specific product by name.
specific_product_by_name = Product.objects.get(name='Laptop')

# Get a specific customer by email. 
specific_customer_by_email = Customer.objects.get(email='test123@gmail.com')

# get a specific category by name.
specific_category_by_name = Category.objects.get(name='Books')

# ***************************Excluding objects********************************

# getting all products except a spefic category.
products_not_in_category = Product.objects.exclude(category__name='Books')

# getting all customers except a specific first name.
customers_not_with_first_name = Customer.objects.exclude(first_name='John')

# getting all products except a specific price.
products_not_with_price = Product.objects.exclude(price=1000.00)

# getting all products except a specific stock value.
products_not_with_stock = Product.objects.exclude(stock=50)

# ***************************Ordering objects********************************

# Get all products ordered by price in ascending order.
products_ordered_by_price_asc = Product.objects.order_by('price')


recent_expensive_products = Product.objects.filter(price__gt=500, 
                      stock__gt=0).order_by('-created_at')[:5]


# Get all customers ordered by joined date in descending order.
customers_ordered_by_joined_date_desc = Customer.objects.order_by('-joined_date')

# complex ordering
# Get all products ordered by category name and then by price in descending order.      
products_ordered_by_category_and_price = Product.objects.order_by('category__name', '-price')

# Get all categories ordered by name in ascending order.
categories_ordered_by_name_asc = Category.objects.order_by('name')

# Get all categories ordered by name in descending order.
categories_ordered_by_name_desc = Category.objects.order_by('-name')

# *******************************End*******************************************


# Updating Objects (save, update, bulk_update)


my_laptop = Product.objects.get(name='Gaming Laptop')
my_laptop.price = 1750.00
my_laptop.save()

# Update multiple products in the database.
products_to_update = Product.objects.filter(category__name='Electronics')
for product in products_to_update:  
    product.price += 100.00  # Increase price by $100       
Product.objects.bulk_update(products_to_update, ['price'])


# bulk_update() allows you to update a batch of objects you already have in memory, in a single query:

products_to_update = list(Product.objects.filter(stock__lt=10))
for p in products_to_update:
    p.stock = 0
Product.objects.bulk_update(products_to_update, ['stock'])

# **************************End*******************************************

# Deleting Objects (delete, bulk_delete)

# Delete a specific category.
category_to_delete = Category.objects.get(name='Books')
category_to_delete.delete()

# Delete a specific product.
product_to_delete = Product.objects.get(name='Laptop')
product_to_delete.delete()

# Delete a specific customer.
customer_to_delete = Customer.objects.get(
    first_name='Aniket',
    last_name='Suryavanshi'
)
customer_to_delete.delete()

# Delete multiple products in the database.
products_to_delete = Product.objects.filter(category__name='Toys')
products_to_delete.delete()

# Delete multiple customers in the database.
customers_to_delete = Customer.objects.filter(first_name='John')
customers_to_delete.delete()

# delete multiple objects in the database.
Product.objects.filter(stock=0).delete()

# **************************End*******************************************


# *******************************Avoiding N+1 Queries Problem********************************

# Optimized Relationship Loading (select_related, prefetch_related)


# 3. N+1 query problem.

#     select_related: For one-to-one or ForeignKey (one-to-many) relationships,
#     this performs a JOIN at the database level to fetch related data in the same query. 
#     It's ideal when the "one side" of the relationship is a single object.


# Without select_related (N+1 problem)


products = Product.objects.all()

for product in products:
    print(f"Product Name : {product.name}., Product Category : {product.category.name}.")

# With select_related (avoids N+1 problem)
# With select_related (a single JOIN query)

products = Product.objects.select_related('category').all()

for product in products:
    print(f"Product Name : {product.name}., Product Category : {product.category.name}.")

    # prefetch_related: For many-to-many or ReverseForeignKey (reverse one-to-many) 
    # relationships, this performs a separate query for the related objects and joins 
    # the results in Python. It's useful when the "many side" of the relationship 
    # has multiple objects. Imagine a Tag model and a ManyToManyField in Product.

product_with_tags = Product.objects.prefetch_related('tags').all()

for product in product_with_tags:
    print(f"Product Name : {product.name}, Tags : {', '.join(tag.name for tag in product.tags.all())}.")

    
# ********************************End*******************************************

# Aggregations (aggregate, annotate)

# aggregate: Performs an aggregation function (SUM, AVG, COUNT, MIN, MAX) over the entire QuerySet and returns a dictionary.




