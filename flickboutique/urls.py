from django.urls import path
from . import views

app_name = 'flickboutique'

urlpatterns = [
    # Template-less URLs
    path("delete-product", views.deleteProduct, name="deleteProduct"),
    path("user-logout", views.userLogout, name="userLogout"),
    path("rate-product", views.rateProduct, name="rateProduct"),
    path("rate-business", views.rateBusiness, name="rateBusiness"),
    path("comment-product", views.commentProduct, name="commentProduct"),
    path("reply-product-comment", views.replyProductComment, name="replyProductComment"),
    path("process-edited-business", views.processEditedBusiness, name="processEditedBusiness"),
    path("add-to-cart", views.addToCart, name="addToCart"),
    path("delete-from-cart", views.deleteFromCart, name="deleteFromCart"),
    path("complete-order-details", views.completeOrderDetails, name="completeOrderDetails"),
    path("add-customer-message", views.addCustomerMessage, name="addCustomerMessage"),
    path("add-business-message", views.addBusinessMessage, name="addBusinessMessage"),

    # URLs with templates
    path("", views.index, name="index"),
    path("customer-signup", views.customerSignup, name="customerSignup"),
    path("customer-signup-success", views.customerSignupSuccess, name="customerSignupSuccess"),
    path("business-signup-success", views.businessSignupSuccess, name="businessSignupSuccess"),
    path("business-signup", views.businessSignup, name="businessSignup"),
    path("customer-login", views.customerLogin, name="customerLogin"),
    path("business-login", views.businessLogin, name="businessLogin"),
    path("customer-home", views.customerHome, name="customerHome"), # This should later be the index if the user is a customer
    path("business-home", views.businessHome, name="businessHome"), # This should later be the index if the user is a business
    path("manage-site", views.manageSite, name="manageSite"),
    path("product-page/<str:productURL>/", views.productPage, name="productPage"), # Business username should later be added
    path("register-product", views.registerProduct, name="registerProduct"),
    path("preview-changes", views.previewSiteChanges, name="previewSiteChanges"),
    path("edit/<str:username>", views.editBusinessProfilePage, name="editBusinessProfilePage"),
    path("cart", views.cart, name="cart"),
    path("payment-processing", views.paymentsProcessing, name="paymentsProcessing"),
    path("view-business-orders", views.viewBusinessOrders, name="viewBusinessOrders"),
    path("view-customer-orders", views.viewCustomerOrders, name="viewCustomerOrders"),
    path("order-complete", views.orderComplete, name="orderComplete"),
    path("messages/<str:business>", views.orderCustomerConversation, name="orderCustomerConversation"),
    path("<str:business>/messages/<str:customer>", views.orderBusinessConversation, name="orderBusinessConversation"),
    path("conversations-list", views.customerConversationsList, name="customerConversationsList"),
    path("<str:business>/conversations-list", views.businessConversationsList, name="businessConversationsList"),

    path("<str:username>", views.businessView, name="businessView"),
]