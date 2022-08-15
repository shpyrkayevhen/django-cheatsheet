# from store.models import Product
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models import Q, F, Func, Value
# from django.db.models.aggregates import Count, Max, Min, Avg, Sum (for work with aggregate obj)


# ---------------------------------------------------------------------------------------------------------------------------------------


# --- (1) RETRIEVING OBJECTS/ОТРИМАННЯ ОБ'ЄКТІВ --- $


# Get all products from table Products -> queryset
"""products = Product.objects.all()"""

# Get only single object with id = 1
"""product = Product.objects.get(id=1).first()"""

# Get quantity products table Product immediately -> int
"""products_quantity = Product.objects.count()"""

# Check exist product with id=1 in table -> True or False
"""product_exist = Product.objects.filter(pk=1).exists()"""


# ---------------------------------------------------------------------------------------------------------------------------------


# --- (2) FILTERING OBJECTS/ФІЛЬТРУВАННЯ ОБ’ЄКТІВ --- $


# Get all products which costs $20
'''products = Product.objects.filter(price=20)'''

# Get all products which greater than > $20
'''products = Product.objects.filter(price__gt=20'''

# Get all products which less than or equal <= $20
'''products = Product.objects.filter(price__elt=20)'''

# Get all products which price between $20 - $50
'''products = Product.objects.filter(price__range=(20,50))'''

# Get all products in collection 2 (relational table Collection ForeignKey)
'''products = Product.objects.filter(collection__id=2)'''

# Get all products in collection where collection id < 4
'''products = Product.objects.filter(collection__id__lt=4)'''

# Get all products with title 'coffee' (key sensitive)
'''products = Product.objects.filter(title__contains="coffee")'''

# Get all products with title 'coffee' (not key sensitive)
'''products = Product.objects.filter(title__icontains="coffee")'''

# Get all products which title start in 'Ab'
'''products = Product.objects.filter(title__startswith="Ab")'''

# Get all products which title end in '.com'
'''products = Product.objects.filter(title__endwith=".com")'''

# Get all products which was updated in 2021 year
'''products = Product.objects.filter(update_at__year=2021)'''

# Get all products without description
'''products = Product.objects.filter(description__isnull=True)'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- COMPLEX LOOKUPS USING Q OBJECT --- $ 👉 from django.db.models import Q


# Коли використовуємо OR оператор, то користуємось Q object.
# Якщо AND то можна використовувати його також, але легше так 👇

# (1) Get all products which price > $20 AND title is 'Iphone'
'''products = Product.objects.filter(price__gt=20,title='Iphone')'''

# (2) Get all products which price > $20 AND title is 'Iphone'
'''Product.objects.filter(price__gt=20).filter(title='Iphone')'''


# Get products which have: inventory < 10 OR price > 20
'''products = Product.objects.filter(Q(inventory__lt=10) | Q(price__gt=20))'''

# Get products which have: inventory < 10 AND price > 20 ('~' - not)
'''products = Product.objects.filter(Q(inventory__lt=1 0) & ~Q(price__lt=20))'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- REFERENCING FIELDS USING F OBJECTS --- $ 👉 from django.db.models import F


# Get products which: inventory = price (column)
'''products = Product.objects.filter(inventory = F('unit_price'))'''

# Також можемо посилатись на поля пов'язаних таблиць
# Get products which fields: product_id = collection_id
'''products = Product.objects.filter(id = F('collection__id'))'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- SORTING DATA --- $


# Отримати всі продукти посортовані в алф. порядку по назві
'''products = Product.objects.order_by('title')'''

# Отримати продукти посортовані від найновіших(від кінця)
'''products = Product.objects.order_by('-id')'''

# Отримати продукти від найсвіжіше оновлених
'''products = Product.objects.order_by('-last_update')'''

# Отримати продукти посортовані за кількома параметрами, спершу по ціні від найдорожчих та їх назві в алф. порядку.
'''products = Product.objects.order_by('-price', 'title')'''

# Отримати об’єкти посортовані від найдешевших до найдорожчих (тому що в кінці вказано .reverse нашого query)
'''products = Product.objects.order_by('-price','title').reverse()'''

# Отримати всі об’єкти з колекції 1 (пов'язана таблиця з Product) та сортувати їх по ціні (від найдешевших до найдорожчих)
'''products=Product.objects.filter('collection__id=1').order_by('price')'''

# Отримати найдорожчий продукт з таблиці (1)
'''product = Product.objects.order_by('-price')[0]'''

# Отримати найдешевний продукт з таблиці (2)
'''product = Product.objects.earliest('price')'''

# Отримати найдорожчий продукт з таблиці (2)
'''product = Product.objects.latest('price')'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- LIMITING RESULTS --- $


# Отримати щоб відобразити перших 5 об’єктів на 1 сторінці
'''product = Product.objects.all()[0:5]'''

# Отримати щоб відобразити наступних 5 об’єктів на 2 сторінці
'''product = Product.objects.all()[5:10]'''

# Отримати 10 найдорожчих продуктів з таблиці
'''products = Product.objects.order_by(‘-price’)[0:10]'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- SELECTING FIELDS TO QUERY --- $

# Отримаємо лише значення колонки id та title усіх продуктів
'''products = Product.objects.values('id', 'title')'''

# Отримаємо назву усіх продуктів, а також назву колекції до якої вони відносяться (пов’язана таблиця collection з product) -> INNER JOIN
'''products = Product.objects.values('title', 'collection__title')'''
# Return after for loop -> ('Iphone', 'Mobile'), ('Macbook', 'Computer')


# Select products that have been ordered and sort them by title 👉 from store.models import ORderItem
'''products = OrderItem.objects.values('product__id')'''

# Ми отримаємо результат з дублікатами продуктів, щоб їх не було до результату queryset values добавляємо метод distinct
'''products = OrderItem.objects.values('product__id').distinct()'''

# Щоб сортувати ці продукти йдемо в таблицю product і сортуємо продукти по id
'''products = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct())'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- DEFERRING FIELDS/ВІДКЛАДЕННЯ ПОЛІВ --- $


# Return instance of Product class. .values() - return data as  a dictionary obj. Be careful with this method!
'''products = Product.objects.only('id', 'title')'''

# Отримаємо продукти з даними окрім колонки з їх описом
'''products = Product.objects.defer('description')'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- SELECTING RELATED OBJECTS --- $

# Використовуємо, коли наша таблиця має Foreign Key(Many-to-One) з пов’язаною таблицею. select_related()
# It's the same: from product Inner Join collection ON ..)
'''products = Product.objects.select_related('collection').all()'''
'''products = Product.objects.select_related('collection__column_name').all()'''

# Можемо зручно витягувати дані пов’язаних таблиць без лишніх запитів до бд
# {% for product in products %}
#	 {{ product.collection.title }}
# {% endfor %}

# # Використовуємо, коли наша таблиця має  Foreign Key(Many-to-Many) з іншої таблицею
'''products = Product.objects.prefetch_related('promotion').all()'''

# Можемо комбінувати, коли в нас є декілька пов’язаних таблиць
'''products = Product.objects.prefetch_related('promotion').select_related('collection').all()'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- AGGREGATING OBJECTS --- $

# Коли потрібно знайти максимальне max/min/avg product price використовуємо .aggregate() метод, в який передаємо aggreg obj
# from django.db.models.aggregates import Count, Max, Min, Avg, Sum

# Count all sum
'''products_price = Product.objects.aggregate(Count('price'))'''

# Count product quantity
'''product = Product.objects.aggregate(Count('id'))'''
'''product = Product.objects.aggregate(count=Count('id'))'''

# Count product quantity and min product price
'''product = Product.objects.aggregate(count=Count('id'), min_pricet=Count('price'))'''

# Порахувати кількість об’єктів в певній колекцій
'''product = Product.objects.filter('collection__id=1').aggregate(count=Count('id'))'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- ANNOTATING OBJECT --- $

# Коли при запиті до бд при повернені даних, потрібно додати або просто потрібно додати до таблиці (класу) нову колонку.
# Аргумент в метод .annotate() можна передавати (NewColumnName = Expression)

# Expression: Value, F, Func, Aggregate(Max, Min…). Це класи які нам потрібно завжди імпортовувавати

# Отримаємо queryset з таблиці Product, в якому кожен продукт матиме додаткову колонку(атрибут) is_new зі значенням 1
'''product = Product.objects.annotate(is_new=Value(1))'''

# # Отримаємо queryset з таблиці Product, в якому кожен продукт матиме додаткову колонку(атрибут) new_id
# з значенням його поточного id або 2-ий приклад
'''product = Product.objects.annotate(new_id=F('id'))'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- CALLING DATABASE FUNCTIONS --- $

'''product=Product.objects.annotate(full_name=Func(F('first_name'),Value(' '),F('last_name'), function='CONCAT')'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- GROUPING DATA --- $


# Хочемо побачити скільки замовлених товарів має customer. Так як в таблиці Order є Foreign Key на Customer,
# то в Customer Django атоматично створює related_name = 'order' (зворотній зв’язок). Ми можемо змінювати
# цю назву вказаваши в властивості customer таблиці Order, додатковий аргумент (related_name=” ”)

'''product=Product.objects.annotate(orders_count=Count('order')'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- WORKING WITH EXPRESSION WRAPPERS --- $ 👉 from django.db.models import ExpressionWrapper

# Використовуємо, коли будуємо комплексний вираз
'''discounted_price = ExpressionWrapper(F('unit_price') * 0.8, uotput_field=DecimalField())'''

'''product=Product.objects.annotate(discounted_price=discounted_price)'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- QUERYING GENERIC RELATIONSHIPS --- $


# Generic (Content Type) моделі(таблиці) з даним зв’язком ми можемо використовувати до будь яких моделей в наших app.
# Перелік всіх моделей наших app з атрибутами (id, app_label, name) ми можемо переглянути в бд Table django_content_type.

# Імпортуємо дані моделей(таблиць) з django_content_type
# from django.contrib.contenttypes.models import ContentType
# from tags.models import TaggedItem
# from store.models import Product

# Знаходимо в таблиці django_content_type (Вбудована модель CoontentType в Django) контент id для моделі Product.
'''content_type=ContentType.objects.get_for_model(Product)'''

# Знайшоши fields нашої моделі Product (id: 11, name: product)
'''queryset=TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=pk)'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- CREATING OBJECTS --- $


# 1 варіант
'''
    collection = Collection()
    collection.title = 'Video Games'
    Тут Foreign Key на продукт в моделі
    collection.featured_product = Product(pk=1)
    collection.save()
'''

# 2 варіант (автоматично створює instance і save())
'''collection = Collection.objects.create(title = 'Video Games', featured_product_id=pk)'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- UPDATING OBJECTS --- $


# 1 варіант

'''
    collection = Collection.objects.get(id=pk)
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1) <- Foreign Key на продукт в моделі
    collection.save())
'''

# 2 варіант автоматично в кінці робить .save()
'''collection = Collection.objects.filter(id=pk).update(title = 'VG', featured_product_id=pk)'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- DELETING OBJECTS --- $


'''collection = Collection.objects.get(id=pk)
   collection.delete()'''


# Видалення декількох об’єктів
'''collections = Collection.objects.filter(id__gt=5).delete()'''


# ------------------------------------------------------------------------------------------------------------------------------------


# --- TRANSACTIONS --- $ 👉 from django.db import transactions

# # Коли ми одразу при запиті робимо декілька дій з різними моделями (таблицями),
# і при створені/зміні одного запису є залежність (послідовність) роботи іншого (з ним одразу).
# Щоб зміни відбулись одразу в двох моделях (які зв’язані)

# def say_hello(request):

#    with transaction.atomic():
#        order = Order()
#        order.customer_id = 1
#        order.save()

#        item = OrderItem()
#        item.order = order
#        item.product_id = 1
#        item.quantity = 10
#        item.unit_price = 100
#        item.save


# ------------------------------------------------------------------------------------------------------------------------------------


# --- EXECUTING RAW SQL QUERIES --- $

'''products = Product.objects.raw('SELECT * FROM store_product')'''
'''products = Product.objects.raw('SELECT id, title FROM store_product')'''

# Ми також можемо підключити з'єднання до нашої бази даних і виконувати операції без обмежень
# from django.db import connection

#    with connection.cursor() as cursor:
#         cursor.execute('All SQL commands: CRUD')
