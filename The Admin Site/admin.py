# --- SETTING UP THE ADMIN SITE --- $

# $ python manage.py createsuperuser
# $ python manage.py changepassword <user_name>

# urls.py 👇

# 1: admin.site.site_header = 'Storefront Admin'
# 2: admin.site.index_title = 'Admin'

# urlpatterns = [path('/admin'), admin.site.urls)]


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- REGISTERING MODELS --- $


# from .models import Product

# (1) admin.site.register(Product) // 1 варіант

# (2) @admin.register(Product)                                      # Always use it!
#     class ProductAdmin(admin.ModelAdmin):
#           pass


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- CUSTOMAMIZING THE LIST PAGE --- $

# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-options

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#       // Created this action below
#       actions = ['clear_inventory']
#       list_display = ['title', 'price', 'inventory_status', 'collection_title']
#       list_editable = ['price']
#       ordering = ['-price', 'title']
#       list_per_page = 10
#       search_fields = ['title__istartswith']
#       // Preload related fields
#       list_select_related = ['collection']


#       // Selecting Related Objects
#       def collection_title(self, product):
#           return product.collection.title

#       // Adding Computed Columns
#       @admin.display(ordering='inventory') // Tell Django how to sort this column
#       def inventory_status(self, product):
#           if product.inventory < 10:
#              return "low"
#           return "OK"

#       // Creating custom actions                            // Те що над list_page (вибрати все, видалити все)
#       @admin.action(description='Clear inventory')
#       def clear_inventory(self, request, queryset)          // request -> http, queryset -> object(products) which user selected
#           updated_count = queryset.update(inventory=0)      // product.inventory = 0
#           self.message_user(                                // default in ModelAdmin
#                             request,
#                             f'{updated_count} products were successfully updated',
#
#                             OR WE CAN SHOW messages.ERROR())


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- OVERRIDING THE BASE QUERYSET --- $


# @admin.register(Collection)
# class CollectionAdmin(admin.ModelAdmin):
#       list_display = ['title', 'products_count']  // Collection doesn't have a field products_count
#
#       @admin.display(ordering='producst_count')
#  (2)  def products_count(self, collection):
#           return.collection.producst_count
#
#       // admin.ModelAdmin has default method 👇
#  (1)  def get_queryset(self, request):
#           return super().get_queryset(request).annotate(
#               producst_count=Count('product')
#           )


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- PROVIDING LINKS TO OTHER PAGES --- $


# from django.urls import reverse, urlencode
# from django.utils.html import format_html

# def products_count(self, collection):
#     url = (
#            reverse("admin:store_product_changelist")        // reverse('admin:app_model_page')
#            + '?' + urlencode({
#                               'collection__id': str(collection.id)
#                              }))
#
#     return format_html(<a href="{}">{}</>, url, product.collection.title)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- ADDING FILTERING TO THE LIST PAGE --- $


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#       ...
#       list_filter = ['collection', 'last_update', InventoryFilter]
#       ....


# $ WE CAN ALSO CREATE OWN FILTERS

# class InventoryFilter(admin.SimpleListFilter):
#     title = 'inventory'
#     parametr_name = 'inventory'
#
#     def lookups(self, request, model_admin):
#         return [('<10', 'Low')]
#
#     def queryset(self, request, queryset: QuerySet):
#         if self.value() == '<10':
#            return queryset.filter(inventory__lt=10)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- CUSTOMAZING MODEL FORMS  --- $ (CRUD)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#       ...
#
#       autocomplete_fields = ['collection']        // Before set in CollectionAdmin -> search_field = ['title']
#       prepopulated_fields = {                     // Автоматично заповнить поле 'slug' на основі даних 'title'
#                               'slug': ['title']
#                             }
#       fields = []                                 // which we want to show
#       exclude = ['promotions']                    // exclude promotions field from Product Form
#       read_only = []
#       ....


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- ADDING DATA VALIDATION TO OUR MODEL FORMS  --- $  -> models.py
#
#
#     from django.core.validators import MinValueValidator
#
#     class Product(models.Model)
#           .....................
#           price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
#           .....................


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- EDITING CHILDREN USING INLINES  --- $


# class OrderItemInline(admin.TabularInline):                // OR can use (admin.StackedInline)
#       autocomplete_fields = ['product']
#       min_num = 1
#       max_num = 10
#       model = models.ModelItem
#       extra = 0
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#       list_display = ['id', 'placed_at', 'customer']
#       inlines = [OrderItemInline]
#       autocomplete_fields = ['customer']


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --- USING GENERIC RELATIONS  --- $ -> from django.contrib.contenttypes.admin import GenericTabularInline


# class TagInline(GenericTabularInline)
#       model = TaggedItem                                 // This class is from another app


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#       .....................
#       autocomplete_fields = ['tag']
#       inlines = [TagInline]
#       .....................


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
