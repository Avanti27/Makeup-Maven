import random

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from maven.models import Products,Cart,Order

import razorpay
# Create your views here.


def register(request):
    context = {}
    if request.method == "POST":
        fname = request.POST["sname"]
        lname = request.POST["lname"]
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        
        if fname == "" or lname == "" or uname == "" or pwd == "":
            context["errmg"] = "Field not empty"
            return render(request, "register.html", context)
        else:
            try:
                u = User.objects.create(
                    password=pwd, username=uname, first_name=fname, last_name=lname
                )
                u.set_password(pwd)
                u.save()
                context["success"] = "user created succesfully"
                return redirect("/login")
            except Exception:
                context["errmsg"] = "user with same username already exist"
                return render(request, "register.html", context)
    else:
        return render(request, "register.html")


def user_login(request):
    context = {}
    if request.method == "POST":
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        # print(uname)
        # print(pwd)
        # return HttpResponse("data fetch succesfully")
        if uname == "" or pwd == "":
            context["errmsg"] = "data cannot be empty"
            return render(request, "login.html", context)
        else:
            u = authenticate(username=uname, password=pwd)
            # print(u)
            # print(u.is_superuser)
            # return HttpResponse("data is fetched")
            if u is not None:
                login(request, u)
                return redirect("/index")

            else:
                context["errmsg"] = "Invalid credentials"
                return render(request, "login.html", context)
    else:
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("/index")


def homeapp(request):
    context = {}
    p = Products.objects.filter(is_active=True)
    context["products"] = p
    return render(request, "index.html", context)




def index(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"contact.html")

def terms(request):
    return render(request,"terms.html")


def privacy(request):
    return render(request,"privacy.html")

# def product(request):
#     context = {}
#     context["products"] = Products.objects.filter()
#     return render(request, "product.html", context)

def foundation(request):
    return render(request,"foundation.html")

def catfilter(request, cv):
    pass
    q1 = Q(is_active=True)
    q2 = Q(category=cv)
    p = Products.objects.filter(q1 & q2)
    context = {}
    context["products"] = p
    return render(request, "product.html", context)



def addtocart(request, pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].username)
        # print(u[0].is_superuser)
        p = Products.objects.filter(id=pid)
        # check product exists or not
        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        context = {}
        context["products"] = p
        if n == 1:
            context["msg"] = "products already exist in cart"
        else:
            c = Cart.objects.create(uid=u[0], pid=p[0])
            c.save()

            context["success"] = "product added succesfully to cart"

        return render(request, "product_details.html", context)
    else:
        return redirect("/login")

def cart(request):
    userid = request.user.id
    c = Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[0].uid)
    # print(c[0].pid.name)
    s = 0
    np = len(c)
    for x in c:
        print(x)
        print(x.pid.price)
        s = s + x.pid.price * x.qty
    context = {}
    context["products"] = c
    context["total"] = s
    context["n"] = np
    return render(request, "cart.html", context)

def remove(request, cid):
    c = Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/cart")

def sort(request, sv):
    if sv == "0":
        col = "price"
    else:
        col = "-price"
    p = Products.objects.filter(is_active=True).order_by(col)
    context = {}
    context["products"] = p
    return render(request, "index.html", context)


def updateqty(request, qv, cid):
    # print(type(qv))
    # return HttpResponse("in update quantity")
    c = Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv == "1":
        t = c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty > 1:
            t = c[0].qty - 1
            c.update(qty=t)
    return redirect("/cart")


def Product_Detail(request, pid):
    context = {}
    context["products"] = Products.objects.filter(id=pid)
    return render(request, "product_details.html", context)


def product(request):
    context = {}
    p = Products.objects.filter(is_active=True)
    context["products"] = p
    return render(request, "product.html", context)


def place_order(request):
    userid = request.user.id
    c = Cart.objects.filter(uid=userid)
    # print(c)
    oid = random.randrange(1000, 9999)
    print("order id:", oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()
        x.delete()
    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    np = len(orders)
    for x in orders:
        s = s + x.pid.price * x.qty
    context = {}
    context["products"] = orders
    context["total"] = s
    context["n"] = np
    context["u"] = orders
    return render(request, "place_order.html", context)


def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    # np=len(c)
    for x in orders:
        # print(x)
        # print(x.pid.price)
        s = s + x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(
        auth=("rzp_test_b7jAps3fOuyVOi", "qoA2i4dzASyBtMVqfNgo1nat")
    )

    data = {"amount": s * 100, "currency": "INR", "receipt": "oid"}
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context["data"] = payment
    x=request.user.username
    context['mail']=x
    return render(request, "pay.html", context)



'''
def sendusermail(request,mail):
    uemail = request.user.username
    print(request.user.is_authenticated)
    uemail=mail
    order_id = request.POST.get('order_id')
    x= f"Makeup Maven - Order Confirmation for Order {order_id}"
    customer_name = request.POST.get('uemail')
    send_mail(
        x,
        customer_name,
        "avantimhatre27@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("Email Succesfully Send")
'''

def payment(request):
    return render(request,'payment.html')