from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomerInfo)
admin.site.register(BusinessInfo)
admin.site.register(Product)
admin.site.register(ProductDepartment)
admin.site.register(Manufacturer)
admin.site.register(ColorScheme)
admin.site.register(ProductComment)
admin.site.register(ProductCommentReply)

admin.site.register(CustomerShoppingCart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Conversation)
admin.site.register(Message)