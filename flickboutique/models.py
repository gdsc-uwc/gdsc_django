from django.db import models
from django_countries.fields import CountryField # Country field model
from phonenumber_field.modelfields import PhoneNumberField # Phone number field model
from django.contrib.auth.models import User # User field model

# Create your models here.

class ColorScheme(models.Model):
    schemeName = models.CharField(max_length=128)
    accentColor = models.CharField(max_length=20, default="#000000")
    backgroundColor = models.CharField(max_length=20, default="#FFFFFF")
    textColor = models.CharField(max_length=20, default="#000000")
    secondaryTextColor = models.CharField(max_length=20, default="#000000")
    productCardColor = models.CharField(max_length=20, default="#FFFFFF")
    productCardGlowColor1 = models.CharField(max_length=20, default="orange")
    productCardGlowColor2 = models.CharField(max_length=20, default="lightblue")
    logo = models.ImageField(default="billbao_logo.png")

    def __str__(self):
        return self.schemeName

class CustomerInfo(models.Model):
    # Signup form information
    # First name, last name, email, password are in user auth
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_user")
    streetAddress = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    suburb = models.CharField(max_length=64)
    postalCode = models.IntegerField()
    country = CountryField()
    birthday = models.DateField()
    phoneNumber = PhoneNumberField()
    # Other information
    bio = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username}) - {self.suburb}, {self.city}"

class BusinessInfo(models.Model):
    # Signup form information
    # First name is business name and is with email, password in user auth
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_user")
    streetAddress = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    suburb = models.CharField(max_length=64)
    postalCode = models.IntegerField()
    country = CountryField()
    phoneNumber = PhoneNumberField()
    # Other information
    bio = models.CharField(max_length=1024)
    colorScheme = models.ForeignKey(ColorScheme, on_delete=models.CASCADE, related_name="business_color_scheme", default=ColorScheme.objects.get(schemeName="bilbaoDefault").pk)
    profilePicture = models.ImageField(default="noPP.svg")
    profileBanner = models.ImageField(default="nobanner.png")
    rating = models.FloatField(default=0)
    totalRatings = models.IntegerField(default=0)
    ratingsSum = models.IntegerField(null=True)
    raters = models.ManyToManyField(User, related_name="business_raters")

    def __str__(self):
        return f"{self.user.first_name} ({self.user.username}), {self.city}"

class ProductDepartment(models.Model):
    departmentName = models.CharField(max_length=128)

    def __str__(self):
        return self.departmentName

class Manufacturer(models.Model):
    manufacturerName = models.CharField(max_length=128)

    def __str__(self):
        return self.manufacturerName

class ProductCommentReply(models.Model):
    replier = models.ForeignKey(User, related_name="comment_replier", on_delete=models.CASCADE, null=True)
    replyBody = models.TextField(null=True, blank=True)

class ProductComment(models.Model):
    commenter = models.ForeignKey(User, related_name="product_commenter", on_delete=models.CASCADE)
    commentBody = models.TextField(null=True, blank=True)
    replies = models.ManyToManyField(ProductCommentReply, related_name="product_replies")


class Product(models.Model):
    productName = models.CharField(max_length=128)
    productURL = models.CharField(max_length=64)
    productDepartment = models.ForeignKey(ProductDepartment, related_name="product_department", on_delete=models.CASCADE)
    productPrice = models.FloatField()
    productInformation = models.CharField(max_length=2048)
    productRating = models.FloatField(default=0)
    productTotalRatings = models.IntegerField(default=0)
    productImage = models.ImageField(null=True)
    productRatingsSum = models.IntegerField(null=True)
    productRaters = models.ManyToManyField(User, related_name="product_raters")
    soldBy = models.ForeignKey(User, related_name="product_seller", on_delete=models.CASCADE, null=True)
    productComments = models.ManyToManyField(ProductComment, related_name="product_comments")

    def __str__(self):
        return self.productName

class CartItem(models.Model):
    
    item = models.ForeignKey(Product, related_name="cart_item", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.item.productName

class CustomerShoppingCart(models.Model):
    buyer = models.ForeignKey(User, related_name="buyer", on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name="shopping_cart_items")

class Order(models.Model):
    buyer = models.ForeignKey(User, related_name="order_maker", on_delete=models.CASCADE)
    business = models.ForeignKey(User, related_name="order_checker", on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name="ordered_items")

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.body

class Conversation(models.Model):
    messages = models.ManyToManyField(Message, related_name="conversation_messages")
    business = models.ForeignKey(User, related_name="business_message", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="customer_message", on_delete=models.CASCADE)

