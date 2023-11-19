from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from maven import views

urlpatterns = [
    path("index/",views.index, name="apphome"),
    path("register",views.register, name="registerform"),
    path("contact",views.contact,name="contactform"),
    path("terms",views.terms,name="termscondition"),
    path("privacy",views.privacy, name="privacyform"),
    path("product",views.product, name="productform"),
    path("foundation",views.foundation, name="foundationform"),
    path("addtocart/<pid>", views.addtocart, name="cartform"),
    path("catfilter/<int:cv>/", views.catfilter, name="catfilter"),
    path("productdetail/<pid>", views.Product_Detail, name="productdetailform"),
    path("place_order", views.place_order,name="order"),
    path("order", views.place_order),
    path("makepayment", views.makepayment),
    #path('sendmail/<mail>/', views.sendusermail, name='sendusermail'),
   
    path("login/", views.user_login, name="loginform"),
    path("logout", views.user_logout, name="logoutform"),
    path("cart",views.cart),
    path("remove/<cid>", views.remove,name="removeitem"),
    path("updateqty/<qv>/<cid>", views.updateqty, name="updateform"),
    path("sort/<str:sv>", views.sort, name="sort"),
    path("payment/", views.payment),
    #path("thankyou",views.thankyou),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)