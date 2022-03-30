from re import T
from django.db import IntegrityError # Username check
from django.shortcuts import render
# URL redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import phonenumbers # Phone number formatting
from . import forms # Forms
from django.contrib.auth import authenticate, login, logout # Authentication
from django.contrib.auth.models import User
from . import models

# Home page
def index(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:customerHome'))

    return render(request, 'flickboutique/landingPage.html')

# Customer signup page
def customerSignup(request):

    form = forms.CustomerSignupForm()

    if request.method == 'POST':
        
        submittedForm = forms.CustomerSignupForm(request.POST)

        if submittedForm.is_valid():

            firstName = submittedForm.cleaned_data['firstName']
            lastName = submittedForm.cleaned_data['lastName']
            userName = submittedForm.cleaned_data['userName']
            email = submittedForm.cleaned_data['email']
            birthday = submittedForm.cleaned_data['birthday']
            streetAddress = submittedForm.cleaned_data['streetAddress']
            city = submittedForm.cleaned_data['city']
            suburb = submittedForm.cleaned_data['suburb']
            postalCode = submittedForm.cleaned_data['postalCode']
            country = submittedForm.cleaned_data['country']
            phoneNumber = submittedForm.cleaned_data['phoneNumber']
            password = submittedForm.cleaned_data['password']
            confirmPassword = submittedForm.cleaned_data['confirmPassword']

            if (password == confirmPassword):
                # User authentication creation
                try:
                    parsed_number = phonenumbers.parse(phoneNumber, country)

                    phoneNumber = phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)

                except IntegrityError: # User already exists
                    context = {
                        'form' : submittedForm,
                        'error': "A user with that username already exists.",
                    }

                    return render(request, 'flickboutique/businessSignup.html', context)
                # Saves user information to database
                user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
                user.save()

                # Other information saved to database
                userInfo = models.CustomerInfo(user=user, streetAddress=streetAddress, birthday=birthday, city=city, country=country, suburb=suburb, postalCode=postalCode, phoneNumber=phoneNumber)
                userInfo.save()

                return HttpResponseRedirect(reverse('flickboutique:customerSignupSuccess'))

            else:
                context = {
                    'form' : submittedForm,
                    'error': "Something went wrong."
                }

                return render(request, 'flickboutique/businessSignup.html', context)

    context = {
        'form' : form,
    }

    return render(request, 'flickboutique/customerSignup.html', context)


# Customer signup success page
def customerSignupSuccess(request):
    return render(request, 'flickboutique/customerSignupSuccess.html')

# Business signup success page
def businessSignupSuccess(request):
    return render(request, 'flickboutique/businessSignupSuccess.html')

# Business signup page
def businessSignup(request):

    form = forms.BusinessSignupForm()

    if request.method == 'POST':
        
        submittedForm = forms.BusinessSignupForm(request.POST)

        if submittedForm.is_valid():

            businessName = submittedForm.cleaned_data['businessName']
            userName = submittedForm.cleaned_data['userName']
            email = submittedForm.cleaned_data['email']
            streetAddress = submittedForm.cleaned_data['streetAddress']
            city = submittedForm.cleaned_data['city']
            suburb = submittedForm.cleaned_data['suburb']
            postalCode = submittedForm.cleaned_data['postalCode']
            country = submittedForm.cleaned_data['country']
            contactNumber = submittedForm.cleaned_data['contactNumber']
            password = submittedForm.cleaned_data['password']
            confirmPassword = submittedForm.cleaned_data['confirmPassword']

            if (password == confirmPassword):
                # User authentication creation
                try:
                    user = User.objects.create_user(first_name=businessName, username=userName, email=email, password=password)
                    user.save()

                except IntegrityError:
                    context = {
                        'form' : submittedForm,
                        'error': "A user with that username already exists."
                    }

                    return render(request, 'flickboutique/businessSignUp.html', context)


                parsed_number = phonenumbers.parse(contactNumber, country)

                contactNumber = phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)
                # Other information saved to database
                userInfo = models.BusinessInfo(user=user, streetAddress=streetAddress, city=city, country=country, suburb=suburb, postalCode=postalCode, phoneNumber=contactNumber)
                userInfo.save()

                return HttpResponseRedirect(reverse('flickboutique:businessSignupSuccess'))

            else:
                context = {
                    'form' : submittedForm,
                    'error': "Something went wrong."
                }

                return render(request, 'flickboutique/businessSignUp.html', context)

    context = {
        'form' : form,
    }

    return render(request, 'flickboutique/businessSignUp.html', context)

# Customer login page
def customerLogin(request):
    form = forms.CustomerLoginForm()

    # When the form is submitted, validate the form
    if request.method == 'POST':

        submittedForm = forms.CustomerLoginForm(request.POST) # User data submitted is stored in form

        if submittedForm.is_valid(): # Server-side validation
            userName = submittedForm.cleaned_data['userName']
            password = submittedForm.cleaned_data['password']

            user = authenticate(username=userName, password=password)

            if user is not None: # If the user is authenticated, they should be logged in
                login(request, user)
                request.session['pageVisits'] = 0
                return HttpResponseRedirect(reverse('flickboutique:customerHome'))
            else:
                return render(request, 'flickboutique/customerLogin.html', {
                    'form' : form,
                    'error' : "Your username or password is incorrect.",
                })
    
    return render(request, 'flickboutique/customerLogin.html', {
        'form' : form,
    })

# Business login form
def businessLogin(request):

    form = forms.BusinessLoginForm()

    # When the form is submitted, validate the form
    if request.method == 'POST':

        submittedForm = forms.BusinessLoginForm(request.POST) # User data submitted is stored in form

        if submittedForm.is_valid(): # Server-side validation
            userName = submittedForm.cleaned_data['userName']
            password = submittedForm.cleaned_data['password']

            user = authenticate(username=userName, password=password)

            if user is not None: # If the user is authenticated, they should be logged in
                login(request, user)
                request.session['pageVisits'] = 0
                return HttpResponseRedirect(reverse('flickboutique:businessHome'))
            else:
                return render(request, 'flickboutique/businessLogin.html', {
                    'form' : form,
                    'error' : "Your username or password is incorrect.",
                })

    context = {
        'form' : form,
    }
    return render(request, 'flickboutique/businessLogin.html', context)

# Customer home page
def customerHome(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    # Checks to see if they are visiting the page for the first time
    request.session['pageVisits'] += 1

    businesses = models.BusinessInfo.objects.all().order_by('-rating')

    business = User.objects.get(username=request.user.username)

    # Gets information about the business
    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'businesses' : businesses,
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'pageVisits': request.session['pageVisits']
    }

    return render(request, 'flickboutique/customerHome.html', context)


# Business home page
def businessHome(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))
    
    request.session['pageVisits'] += 1

    products = models.Product.objects.filter(soldBy=request.user)

    try:
        userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)
    except (KeyError, models.BusinessInfo.DoesNotExist):
        userBusinessInfo = None

    context = {
        'products' : products,
        'businessInfo': userBusinessInfo,
        'userBusinessInfo': userBusinessInfo,
        'pageVisits': request.session['pageVisits']
    }

    return render(request, 'flickboutique/businessHome.html', context)

# Product information page
def productPage(request, productURL):

    try:
        userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)
    except models.BusinessInfo.DoesNotExist:
        userBusinessInfo = None

    context = {
        'product': models.Product.objects.get(productURL=productURL),
        'businessInfo': userBusinessInfo,
        'userBusinessInfo': userBusinessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault")
    }

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'), context)

    return render(request, 'flickboutique/productPage.html', context)

# Business store page
def businessView(request, username):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    businessUser = User.objects.get(username=username)

    products = models.Product.objects.filter(soldBy=businessUser)


    try:
        userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)
    except (KeyError, models.BusinessInfo.DoesNotExist):
        userBusinessInfo = None

    context = {
        'products' : products,
        'business': businessUser,
        'businessInfo': models.BusinessInfo.objects.get(user=businessUser),
        'userBusinessInfo': userBusinessInfo,
    }

    return render(request, 'flickboutique/businessView.html', context)

# Product registration page
def registerProduct(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    if request.method == 'POST':

        submittedForm = forms.ProductRegistrationForm(request.POST, request.FILES)

        print(request.FILES)

        if submittedForm.is_valid():
            productName = submittedForm.cleaned_data['productName']
            productDepartment = submittedForm.cleaned_data['productDepartment']
            productPrice = submittedForm.cleaned_data['productPrice']
            productInformation = submittedForm.cleaned_data['productInformation']
            productImage = request.FILES['productImage']
            productURL = productName.replace(' ', '-')
            # Registers product onto database
            newProduct = models.Product.objects.create(productName=productName, productDepartment=models.ProductDepartment.objects.get(id=productDepartment), productPrice=productPrice, productImage=productImage, productInformation=productInformation, productURL=productURL, soldBy=request.user)
            newProduct.save()

            return HttpResponseRedirect(reverse("flickboutique:businessHome"))
        else:
            context = {
                'form' : forms.ProductRegistrationForm(),
                'error' : 'Something went wrong.'
            }
            return render(request, 'flickboutique/registerProduct.html', context)
        


    context = {
        'form' : forms.ProductRegistrationForm()
    }

    return render(request, 'flickboutique/registerProduct.html', context)

# Preview changes made to site
def previewSiteChanges(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    if request.method == 'GET': # Fetches information of color inputs
        accentColor = request.GET.get('accentColor')
        backgroundColor = request.GET.get('backgroundColor')
        textColor = request.GET.get('textColor')
        secondaryTextColor = request.GET.get('secondaryTextColor')
        productCardColor = request.GET.get('productCardColor')
        productCardGlowColor1 = request.GET.get('productCardGlowColor1')
        productCardGlowColor2 = request.GET.get('productCardGlowColor2')

        userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)

        # Readies color information to be displayed on page
        context = {
            'accentColor': accentColor,
            'backgroundColor': backgroundColor,
            'textColor': textColor,
            'secondaryTextColor': secondaryTextColor,
            'productCardColor': productCardColor,
            'productCardGlowColor1': productCardGlowColor1,
            'productCardGlowColor2': productCardGlowColor2,
            'businessInfo': userBusinessInfo,
            'userBusinessInfo': userBusinessInfo,
        }

        return render(request, 'flickboutique/previewSiteChanges.html', context)

    if request.method == 'POST':

        accentColor = request.POST.get('accentColor')
        backgroundColor = request.POST.get('backgroundColor')
        textColor = request.POST.get('textColor')
        secondaryTextColor = request.POST.get('secondaryTextColor')
        productCardColor = request.POST.get('productCardColor')
        productCardGlowColor1 = request.POST.get('productCardGlowColor1')
        productCardGlowColor2 = request.POST.get('productCardGlowColor2')

        user = models.BusinessInfo.objects.get(user=request.user)
        # Saves color scheme information to database if it doesn't exist
        if user.colorScheme.schemeName != request.user.username:
            scheme = models.ColorScheme.objects.create(schemeName=request.user.username, accentColor=accentColor, backgroundColor=backgroundColor, textColor=textColor, secondaryTextColor=secondaryTextColor, productCardColor=productCardColor, productCardGlowColor1=productCardGlowColor1, productCardGlowColor2=productCardGlowColor2)
            scheme.save()
            user.colorScheme = scheme
            user.save()
        else:
            # Overwrites information if it does exist
            user.colorScheme.accentColor = accentColor
            user.colorScheme.backgroundColor = backgroundColor
            user.colorScheme.textColor = textColor
            user.colorScheme.secondaryTextColor = secondaryTextColor
            user.colorScheme.productCardColor = productCardColor
            user.colorScheme.productCardGlowColor1 = productCardGlowColor1
            user.colorScheme.productCardGlowColor2 = productCardGlowColor2
            user.colorScheme.save()
            user.save()
            

        return HttpResponseRedirect(reverse("flickboutique:businessHome"))


    return render(request, 'flickboutique/previewSiteChanges.html')

# Site management page, where user can make changes to the color scheme
def manageSite(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)

    if request.method == 'POST':
        if request.POST.get('logoChange'):
            logo = request.FILES['logo']
            userinfo = models.BusinessInfo.objects.get(user=User.objects.get(username=request.user.username))
            userinfo.colorScheme.logo = logo
            userinfo.colorScheme.save()
        if request.POST.get('fontChange'):
            fontName = request.POST['font']
            font = fontName.replace(' ', '+')

            userinfo = models.BusinessInfo.objects.get(user=User.objects.get(username=request.user.username))
            userinfo.colorScheme.font = font
            userinfo.colorScheme.fontName = fontName
            userinfo.colorScheme.save()


        return HttpResponseRedirect(reverse('flickboutique:businessHome'))

    context = {
        'businessInfo': userBusinessInfo,
        'userBusinessInfo': userBusinessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault")
    }
   
    return render(request, 'flickboutique/manageSite.html', context)

# Logs out the user
def userLogout(request):
    logout(request)
    request.session['pageVisits'] = None
    return HttpResponseRedirect(reverse('flickboutique:index'))

# Deletes sold product from database
def deleteProduct(request):
    if request.method == 'POST':
        deletingProduct = request.POST.get('productURL')
        models.Product.objects.get(productURL=deletingProduct).delete()
        return HttpResponseRedirect(reverse('flickboutique:businessHome'))

# Function for handling the rating of a product
def rateProduct(request):
    if request.method == 'POST':
        productName = request.POST.get('productName')
        productRating = int(request.POST.get('productRating'))
        product = models.Product.objects.get(productName=productName)

        # Fetch model values
        if product.productRatingsSum:
            sumRatings = product.productRatingsSum
        else:
            sumRatings = 0
            
        totalRatings = product.productTotalRatings

        # Update model values
        sumRatings += productRating
        totalRatings += 1

        product.productRatingsSum = sumRatings
        newRating = sumRatings / totalRatings
        product.productRating = newRating
        product.productTotalRatings = totalRatings
        product.productRaters.add(request.user)
        product.save()


        return HttpResponseRedirect(reverse('flickboutique:productPage', kwargs={'productURL': product.productURL}))

# Function for handling the rating of a business
def rateBusiness(request):
    if request.method == 'POST':
        businessName = request.POST.get('businessName')
        businessRating = int(request.POST.get('businessRating'))
        business = models.BusinessInfo.objects.get(user=User.objects.get(username=businessName))

        # Fetch model values
        if business.ratingsSum:
            sumRatings = business.ratingsSum
        else:
            sumRatings = 0
            
        totalRatings = business.totalRatings

        # Update model values
        sumRatings += businessRating
        totalRatings += 1

        business.ratingsSum = sumRatings
        newRating = sumRatings / totalRatings
        business.rating = newRating
        business.totalRatings = totalRatings
        business.raters.add(request.user)
        business.save()


        return HttpResponseRedirect(reverse('flickboutique:businessView', kwargs={'username': business.user.username}))

# Function for handling the posting of a comment
def commentProduct(request):
    if request.method == 'POST':
        commenter = request.POST.get('commenter')
        commentBody = request.POST.get('commentBody')
        product = request.POST.get('product')

        userCommenter = models.User.objects.get(username=commenter)
        productCommented = models.Product.objects.get(productURL=product)
        newComment = models.ProductComment.objects.create(commenter=userCommenter, commentBody=commentBody)
        newComment.save()

        productCommented.productComments.add(newComment)
        productCommented.save()

        return HttpResponseRedirect(reverse('flickboutique:productPage', kwargs={'productURL': productCommented.productURL}))

# Function for handling the posting of a reply to a comment
def replyProductComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        replier = request.POST.get('replier')
        replyBody = request.POST.get('replyBody')
        product = request.POST.get('product')

        userReplier = models.User.objects.get(username=replier)
        productCommented = models.Product.objects.get(productURL=product)
        newReply = models.ProductCommentReply.objects.create(replier=userReplier, replyBody=replyBody)
        newReply.save()
        commentModel = models.ProductComment.objects.get(id=comment)
        commentModel.replies.add(newReply)
        commentModel.save()

        return HttpResponseRedirect(reverse('flickboutique:productPage', kwargs={'productURL': productCommented.productURL}))

# Edit business information page
def editBusinessProfilePage(request, username):

    if username == request.user.username:
        business = models.User.objects.get(username=username)
        businessInfo = models.BusinessInfo.objects.get(user=business)

        context = {
            'business': business,
            'businessInfo': businessInfo,
            'userBusinessInfo': businessInfo
        }

        return render(request, 'flickboutique/editBusinessProfilePage.html', context)
    else:
        return HttpResponse("You don't have permission to access this page.")

# Function for handling any edited information about a business
def processEditedBusiness(request):

    if request.method == 'POST':
        # Changes business name
        if request.POST.get('changeBusinessName'):
            businessName = request.POST.get('editBusinessName')
            user = User.objects.get(username=request.user.username)
            user.first_name = businessName
            user.save()

        # Changes username sitewide
        if request.POST.get('changeUsername'):
            username = request.POST.get('editUsername')
            user = User.objects.get(username=request.user.username)
            user.username = username
            user.save()

        # Changes profile picture
        if request.POST.get('changeProfilePicture'):
            profilePicture = request.FILES['editProfilePicture']
            business = models.BusinessInfo.objects.get(user=request.user)
            business.profilePicture = profilePicture
            business.save()

        # Changes banner picture on website
        if request.POST.get('changeProfileBanner'):
            profileBanner = request.FILES['editProfileBanner']
            business = models.BusinessInfo.objects.get(user=request.user)
            business.profileBanner = profileBanner
            business.save()

        # Changes business bio
        if request.POST.get('changeBio'):
            bio = request.POST.get('editBio')
            business = models.BusinessInfo.objects.get(user=request.user)
            print("Bio edit success")
            business.bio = bio
            business.save()

        # Changes address
        if request.POST.get('changeAddress'):
            streetAddress = request.POST.get('editStreetAddress')
            city = request.POST.get('editCity')
            suburb = request.POST.get('editSuburb')
            postalCode = request.POST.get('editPostalCode')
            business = models.BusinessInfo.objects.get(user=request.user)
            business.streetAddress = streetAddress
            business.city = city
            business.suburb = suburb
            business.postalCode = postalCode
            business.save()
        
    return HttpResponseRedirect(reverse('flickboutique:businessHome'))


# Shopping cart display page

def cart(request):

    try:
        cart = models.CustomerShoppingCart.objects.get(buyer=request.user)
    except models.CustomerShoppingCart.DoesNotExist:
        cart = None
    
    # Computing total price
    
    totalPrice = 0
    
    try:
        cartItems = cart.items.all()

        for item in cartItems:
            price = item.item.productPrice
            totalPrice += price * item.quantity
    except AttributeError:
        totalPrice = 0

    business = User.objects.get(username=request.user.username)

    # Fetch business information

    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'cart': cart,
        'totalPrice': totalPrice,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
    }

    return render(request, 'flickboutique/cart.html', context)


# Function for handling addition of products to cart
def addToCart(request):
    if request.method == 'POST':
        try:
            cart = models.CustomerShoppingCart.objects.get(buyer=request.user)
        except models.CustomerShoppingCart.DoesNotExist:
            cart = models.CustomerShoppingCart.objects.create(buyer=request.user)
            cart.save()
        finally:
            productURL = request.POST.get('productURL')
            buyQuantity = request.POST.get('buyQuantity')
            product = models.Product.objects.get(productURL=productURL)
            cart = models.CustomerShoppingCart.objects.get(buyer=request.user)
            cartItem = models.CartItem.objects.create(item=product)
            cartItem.quantity = buyQuantity
            cartItem.save()
            cart.items.add(cartItem)
            cart.save()

    return HttpResponseRedirect(reverse('flickboutique:cart'))

# Function for handling the deletion of a product from the cart
def deleteFromCart(request):
    if request.method == 'POST':
        cart = models.CustomerShoppingCart.objects.get(buyer=request.user)
        cart.items.remove(models.CartItem.objects.get(id=request.POST.get('cartItemId')))
        models.CartItem.objects.filter(id=request.POST.get('cartItemId')).delete()
        cart.save()

    return HttpResponseRedirect(reverse('flickboutique:cart'))


# Payments processing page (this does nothing for now)
def paymentsProcessing(request):

    return render(request, "flickboutique/paymentsProcessing.html")


# Completes the order processing and adds that to the list of orders on a database for a business
def completeOrderDetails(request):

    orderCart = models.CustomerShoppingCart.objects.get(buyer=request.user)

    # Creates an order in the database if one does not already exist for a particular business
    for item in orderCart.items.all():
        try:
            order = models.Order.objects.get(buyer=request.user, business=item.item.soldBy)
        except models.Order.DoesNotExist:
            order = models.Order.objects.create(buyer=request.user, business=item.item.soldBy)
        
        order.items.add(item)
        order.save()

    models.CustomerShoppingCart.objects.filter(buyer=request.user).delete()

    return HttpResponseRedirect(reverse('flickboutique:successfulPayment'))

# View for notifying user of a successful payment
def successfulPayment(request):

    return render(request, "flickboutique/successfulPayment.html")


# View all orders made to a business per customer
def viewBusinessOrders(request):
    
    orders = models.Order.objects.filter(business=request.user)

    business = models.User.objects.get(username=request.user.username)
    businessInfo = models.BusinessInfo.objects.get(user=business)

    context = {
        'orders': orders,
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
    }

    return render(request, 'flickboutique/viewBusinessOrders.html', context)


# View all orders for items bought per business
def viewCustomerOrders(request):
    
    orders = models.Order.objects.filter(buyer=request.user)

    business = User.objects.get(username=request.user.username)

    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'orders': orders,
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault")
    }

    return render(request, 'flickboutique/viewCustomerOrders.html', context)


# Processing the completion of an order, deletes the order from database
def orderComplete(request):
    if request.method == 'POST':
        order = models.Order.objects.get(buyer=User.objects.get(username=request.POST.get('orderBuyer')), business=request.user)
        for item in order.items.all():
            item.delete()

        order.delete()
    return HttpResponseRedirect(reverse('flickboutique:viewBusinessOrders'))


# Basic messaging page and system on customer side
def orderCustomerConversation(request, business):
    try:
        conversation = models.Conversation.objects.get(business=User.objects.get(username=business), customer=request.user)
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create(business=User.objects.get(username=business), customer=request.user)
        conversation.save()

    business = User.objects.get(username=request.user.username)

    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'conversation': conversation
    }
    
    return render(request, 'flickboutique/orderCustomerConversation.html', context)


# Function for handling the sending of a new message from the customer
def addCustomerMessage(request):
    if request.method == 'POST':
        business = request.POST.get('business')
        newMessage = models.Message.objects.create(sender=request.user, body=request.POST.get('sentMessage'))
        conversation = models.Conversation.objects.get(business=User.objects.get(username=business), customer=request.user).messages.add(newMessage)
        newMessage.save()
        conversation.save()

    
        return HttpResponseRedirect(reverse('flickboutique:orderCustomerConversation', kwargs={'business': business}))


# Basic messaging page and system on business side
def orderBusinessConversation(request, business, customer):
    try:
        conversation = models.Conversation.objects.get(business=request.user, customer=User.objects.get(username=customer))
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create(business=request.user, customer=User.objects.get(username=customer))
        conversation.save()

    business = User.objects.get(username=request.user.username)

    businessInfo = models.BusinessInfo.objects.get(user=business)

    context = {
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'conversation': conversation
    }
    
    return render(request, 'flickboutique/orderBusinessConversation.html', context)


# Function for handling the sending of a new message from the business
def addBusinessMessage(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        newMessage = models.Message.objects.create(sender=request.user, body=request.POST.get('sentMessage'))
        conversation = models.Conversation.objects.get(business=request.user, customer=User.objects.get(username=customer)).messages.add(newMessage)
        newMessage.save()
        conversation.save()

        return HttpResponseRedirect(reverse('flickboutique:orderBusinessConversation', kwargs={'customer': customer, 'business': request.user.username}))


# Page for displaying customer conversations
def customerConversationsList(request):
    conversations = models.Conversation.objects.filter(customer=request.user)

    business = User.objects.get(username=request.user.username)

    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'conversations': conversations
    }

    return render(request, 'flickboutique/customerConversationsList.html', context)


# View for displaying business conversations
def businessConversationsList(request, business):
    conversations = models.Conversation.objects.filter(business=request.user)

    business = User.objects.get(username=request.user.username)

    try:
        businessInfo = models.BusinessInfo.objects.get(user=business)
    except models.BusinessInfo.DoesNotExist:
        businessInfo = None

    context = {
        'business': business,
        'businessInfo': businessInfo,
        'userBusinessInfo': businessInfo,
        'defaultScheme': models.ColorScheme.objects.get(schemeName="bilbaoDefault"),
        'conversations': conversations
    }

    return render(request, 'flickboutique/businessConversationsList.html', context)