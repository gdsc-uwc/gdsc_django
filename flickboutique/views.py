from re import T
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models

# Create your views here.

def index(request):
    return render(request, 'flickboutique/landingPage.html')


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
                user = User.objects.create_user(first_name=firstName, last_name=lastName, username=userName, email=email, password=password)
                user.save()

                # Other information saved to database
                userInfo = models.CustomerInfo(user=user, streetAddress=streetAddress, birthday=birthday, city=city, country=country, suburb=suburb, postalCode=postalCode, phoneNumber=phoneNumber)
                userInfo.save()

                return HttpResponseRedirect(reverse('flickboutique:customerSignupSuccess'))

    context = {
        'form' : form,
    }

    return render(request, 'flickboutique/customerSignup.html', context)


def customerSignupSuccess(request):
    return render(request, 'flickboutique/customerSignupSuccess.html')


def businessSignupSuccess(request):
    return render(request, 'flickboutique/businessSignupSuccess.html')


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
                user = User.objects.create_user(first_name=businessName, username=userName, email=email, password=password)
                user.save()

                # Other information saved to database
                userInfo = models.BusinessInfo(user=user, streetAddress=streetAddress, city=city, country=country, suburb=suburb, postalCode=postalCode, phoneNumber=contactNumber)
                userInfo.save()

                return HttpResponseRedirect(reverse('flickboutique:businessSignupSuccess'))

    context = {
        'form' : form,
    }

    return render(request, 'flickboutique/businessSignup.html', context)


def customerLogin(request):
    form = forms.CustomerLoginForm()

    # When the form is submitted, validate the form
    if request.method == 'POST':

        submittedForm = forms.CustomerLoginForm(request.POST) # User data submitted is stored in form

        if submittedForm.is_valid(): # Server-side validation
            userName = submittedForm.cleaned_data['userName']
            password = submittedForm.cleaned_data['password']

            user = authenticate(username=userName, password=password)

            if user is not None:
                login(request, user)
                request.session['pageVisits'] = 0
                return HttpResponseRedirect(reverse('flickboutique:customerHome'))
            else:
                return render(request, 'flickboutique/customerLogin.html', {
                    'form' : form,
                    'error' : "User does not exist.",
                })
    
    return render(request, 'flickboutique/customerLogin.html', {
        'form' : form,
    })


def businessLogin(request):

    form = forms.BusinessLoginForm()

    # When the form is submitted, validate the form
    if request.method == 'POST':

        submittedForm = forms.BusinessLoginForm(request.POST) # User data submitted is stored in form

        if submittedForm.is_valid(): # Server-side validation
            userName = submittedForm.cleaned_data['userName']
            password = submittedForm.cleaned_data['password']

            user = authenticate(username=userName, password=password)

            if user is not None:
                login(request, user)
                request.session['pageVisits'] = 0
                return HttpResponseRedirect(reverse('flickboutique:businessHome'))
            else:
                return render(request, 'flickboutique/businessLogin.html', {
                    'form' : form,
                    'error' : "User does not exist.",
                })

    context = {
        'form' : form,
    }
    return render(request, 'flickboutique/businessLogin.html', context)


def customerHome(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    request.session['pageVisits'] += 1

    businesses = models.BusinessInfo.objects.all().order_by('-rating')

    business = User.objects.get(username=request.user.username)

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


def previewSiteChanges(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    if request.method == 'GET':
        accentColor = request.GET.get('accentColor')
        backgroundColor = request.GET.get('backgroundColor')
        textColor = request.GET.get('textColor')
        secondaryTextColor = request.GET.get('secondaryTextColor')
        productCardColor = request.GET.get('productCardColor')
        productCardGlowColor1 = request.GET.get('productCardGlowColor1')
        productCardGlowColor2 = request.GET.get('productCardGlowColor2')

        userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)


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

        if user.colorScheme.schemeName != request.user.username:
            scheme = models.ColorScheme.objects.create(schemeName=request.user.username, accentColor=accentColor, backgroundColor=backgroundColor, textColor=textColor, secondaryTextColor=secondaryTextColor, productCardColor=productCardColor, productCardGlowColor1=productCardGlowColor1, productCardGlowColor2=productCardGlowColor2)
            scheme.save()
            user.colorScheme = scheme
            user.save()
        else:
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


def manageSite(request):

    # Return to landing page if user is not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('flickboutique:index'))

    userBusinessInfo = models.BusinessInfo.objects.get(user=request.user)

    if request.method == 'POST':
        logo = request.FILES['logo']
        userinfo = models.BusinessInfo.objects.get(user=User.objects.get(username=request.user.username))
        userinfo.colorScheme.logo = logo
        userinfo.colorScheme.save()

        return HttpResponseRedirect(reverse('flickboutique:businessHome'))


    
    context = {
        'businessInfo': userBusinessInfo,
        'userBusinessInfo': userBusinessInfo
    }
   
    return render(request, 'flickboutique/manageSite.html', context)


def userLogout(request):
    logout(request)
    request.session['pageVisits'] = None
    return HttpResponseRedirect(reverse('flickboutique:index'))


def deleteProduct(request):
    if request.method == 'POST':
        deletingProduct = request.POST.get('productURL')
        models.Product.objects.get(productURL=deletingProduct).delete()
        return HttpResponseRedirect(reverse('flickboutique:businessHome'))


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
        return HttpResponse("Hey, you aren't supposed to be here!")


def processEditedBusiness(request):

    if request.method == 'POST':

        if request.POST.get('changeBusinessName'):
            businessName = request.POST.get('editBusinessName')
            user = User.objects.get(username=request.user.username)
            user.first_name = businessName
            user.save()

        if request.POST.get('changeUsername'):
            username = request.POST.get('editUsername')
            user = User.objects.get(username=request.user.username)
            user.username = username
            user.save()

        if request.POST.get('changeProfilePicture'):
            profilePicture = request.FILES['editProfilePicture']
            business = models.BusinessInfo.objects.get(user=request.user)
            business.profilePicture = profilePicture
            business.save()

        if request.POST.get('changeProfileBanner'):
            profileBanner = request.FILES['editProfileBanner']
            business = models.BusinessInfo.objects.get(user=request.user)
            business.profileBanner = profileBanner
            business.save()
        
        if request.POST.get('changeBio'):
            bio = request.POST.get('editBio')
            business = models.BusinessInfo.objects.get(user=request.user)
            print("Bio edit success")
            business.bio = bio
            business.save()

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

def deleteFromCart(request):
    if request.method == 'POST':
        cart = models.CustomerShoppingCart.objects.get(buyer=request.user)
        cart.items.remove(models.CartItem.objects.get(id=request.POST.get('cartItemId')))
        models.CartItem.objects.filter(id=request.POST.get('cartItemId')).delete()
        cart.save()

    return HttpResponseRedirect(reverse('flickboutique:cart'))

def paymentsProcessing(request):

    return render(request, "flickboutique/paymentsProcessing.html")

def completeOrderDetails(request):

    orderCart = models.CustomerShoppingCart.objects.get(buyer=request.user)

    for item in orderCart.items.all():
        try:
            order = models.Order.objects.get(buyer=request.user, business=item.item.soldBy)
        except models.Order.DoesNotExist:
            order = models.Order.objects.create(buyer=request.user, business=item.item.soldBy)
        
        order.items.add(item)
        order.save()

    models.CustomerShoppingCart.objects.filter(buyer=request.user).delete()

    return HttpResponseRedirect(reverse('flickboutique:customerHome'))

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

def orderComplete(request):
    if request.method == 'POST':
        order = models.Order.objects.get(buyer=User.objects.get(username=request.POST.get('orderBuyer')), business=request.user)
        for item in order.items.all():
            item.delete()

        order.delete()
    return HttpResponseRedirect(reverse('flickboutique:viewBusinessOrders'))

def orderCustomerConversation(request, business):
    try:
        conversation = models.Conversation.objects.get(business=User.objects.get(username=business), customer=request.user)
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create(business=User.objects.get(username=business), customer=request.user)

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

def addCustomerMessage(request):
    if request.method == 'POST':
        business = request.POST.get('business')
        newMessage = models.Message.objects.create(sender=request.user, body=request.POST.get('sentMessage'))
        models.Conversation.objects.get(business=User.objects.get(username=business), customer=request.user).messages.add(newMessage)
    
        return HttpResponseRedirect(reverse('flickboutique:orderCustomerConversation', kwargs={'business': business}))


def orderBusinessConversation(request, business, customer):
    try:
        conversation = models.Conversation.objects.get(business=request.user, customer=User.objects.get(username=customer))
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create(business=request.user, customer=User.objects.get(username=customer))

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

def addBusinessMessage(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        newMessage = models.Message.objects.create(sender=request.user, body=request.POST.get('sentMessage'))
        models.Conversation.objects.get(business=request.user, customer=User.objects.get(username=customer)).messages.add(newMessage)
    
        return HttpResponseRedirect(reverse('flickboutique:orderBusinessConversation', kwargs={'customer': customer, 'business': request.user.username}))

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