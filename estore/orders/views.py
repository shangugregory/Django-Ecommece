from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm 
import datetime
from .models import Order, Payment, OrderProduct
from store.models import Product
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

def Payments(request):
    body =  json.loads(request.body)
    print(body)
    order=Order.objects.get(is_ordered = False, order_number = body['orderID'])
    #Store transaction details inside thepayment medel
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    #Move the cart items to rder product tabe
    cart_items = CartItem.objects.filter(user = request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variation.all()
        order_product = OrderProduct.objects.get(id = orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

    #reduse the quantity of sold products
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear cart
    CartItem.objects.filter(user = request.user).delete()
    #send order receaved to the customer
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_recieved_email.html', {
        'user':request.user,
        'order':order,                
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to = [to_email])
    send_email.send()
    #send order data and transaction id back
    
    return render(request, 'orders/payments.html')
    

def Place_order(request, total = 0, quantity = 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax= 0

    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total= total + tax

    if request.method =='POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax=tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number= order_number
            data.save()
            print("Order saved successfully:", request.user)

            
            order = Order.objects.get(is_ordered = False, order_number = order_number)
            context= {
                'order': order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total
            }
            return render(request, 'orders/payments.html', context)
        else:
            # Handle the case where the form is not valid
            # You might want to render the form again with validation errors
            print(" error->", form.errors)
            return HttpResponse(form.errors)

    else:
        return redirect('checkout')


