from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
from django.http import JsonResponse
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import JsonResponse



stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = "http://localhost:8000"

def validate_signup(request):
	email=request.GET.get('email')
	data={
	'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(data.get('amount', 0))  # changed from 'post_data'
            final_amount = amount * 100  # convert to paisa for Stripe

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Cart Payment',
                        },
                        'unit_amount': final_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )

            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
def success(request):
    if 'email' not in request.session:
        return redirect('login')  # or your login route

    user = User.objects.get(email=request.session['email'])
    carts = Cart.objects.filter(user=user, payment_status=False)

    for cart in carts:
        cart.payment_status = True
        cart.save()

    request.session['cart_count'] = Cart.objects.filter(user=user, payment_status=False).count()
    
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')
   
def index(request):
	products=Product.objects.all()
	return render (request,'index.html',{'products':products})
def seller_index(request):
    return render(request,'seller-index.html')	


# Create your views here.
def checkout(request):
	return render (request,'checkout.html')
def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="email already"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					    fname=request.POST['fname'],
					    lname=request.POST['lname'],
					    email=request.POST['email'],
					    mobile=request.POST['mobile'],
					    address=request.POST['address'],
					    password=request.POST['password'],
					    profile_pic=request.FILES['profile_pic'],
					    usertype=request.POST['usertype']
					)
				msg="usrr signup succed"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="pass and c pass nor matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render (request,'signup.html')	
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)

            if user.password == password:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                request.session['profile_pic'] = user.profile_pic.url


                if user.usertype == "buyer":
                	wishlists=Wishlist.objects.filter(user=user)
                	request.session['wishlist_count']=len(wishlists)
                	cart=Cart.objects.filter(user=user,payment_status=False)
                	request.session['cart_count']=len(cart)
                	return render(request, 'index.html')
                else:
                    return render(request, 'seller-index.html')
            else:
                msg = "Incorrect password"
                return render(request, 'login.html', {'msg': msg})

        except User.DoesNotExist:
            msg = "Email not registered"
            return render(request, 'login.html', {'msg': msg})

    return render(request, 'login.html')
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def change_password(request):
    user = User.objects.get(email=request.session['email'])
    
    if request.method == "POST":
        if user.password == request.POST['oldpassword']:
            if request.POST['newpassword'] == request.POST['cpassword']:
                user.password = request.POST['newpassword']
                user.save()
                return redirect('logout')
            else:
                msg = "New password and confirm password do not match."
        else:
            msg = "Old password is incorrect."

        if user.usertype == "buyer":
            return render(request, 'change-password.html', {'msg': msg})
        else:
            return render(request, 'change-password', {'msg': msg})
    
    else:
        if user.usertype == "buyer":
            return render(request, 'change-password.html')
        else:
            return render(request, 'change-password.html')

        
def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.address=request.POST['address']
		user.mobile=request.POST['mobile']
		try:
			User.profile_pic=request.FILES['profile_pic']
		except:
			pass
		msg="profile updatwewd succed"
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="buyer":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})
def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
			    seller=seller,
			    product_category=request.POST['product_category'],
			    product_name=request.POST['product_name'],
			    product_price=request.POST['product_price'],
			    product_desc=request.POST['product_desc'],
			    product_image=request.FILES['product_image'],
			)
		msg="product Added succesfully"
		return render(request,'seller-add-product.html',{'msg':msg})
		
	else:
		return render(request,'seller-add-product.html')
def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})
def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})
def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="product updated succesfully"
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})
def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')
def seller_view_laptop(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Laptop")
	return render(request,'seller-view-product.html',{'products':products})
def seller_view_camera(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="camera")
	return render(request,'seller-view-product.html',{'products':products})
def seller_view_acsessories(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Acsessories")
	return render(request,'seller-view-product.html',{'products':products})	
def product_details(request, pk):
    wishlist_flag = False
    cart_flag = False
    product = Product.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])

    # Check Wishlist
    if Wishlist.objects.filter(user=user, product=product).exists():
        wishlist_flag = True

    # Check Cart
    if Cart.objects.filter(user=user, product=product,payment_status=False).exists():
        cart_flag = True

    return render(request, 'product-details.html', {
        'product': product,
        'wishlist_flag': wishlist_flag,
        'cart_flag': cart_flag
    })

 
def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')
def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')
	
def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price
		)
	return redirect('cart')
def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	for i in carts:
		net_price=net_price+i.total_price
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product,payment_status=False)
	cart.delete()
	return redirect('cart')

def change_qty(request):
	pk=int(request.POST['pk'])
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render (request,'myorder.html',{'carts':carts})
def seller_view_order(request):
	myorder=[]
	seller=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(payment_status=True)
	for i in carts:
		if i.product.seller == seller:
			myorder.append(i)
	return render (request,'seller-view-order.html',{'myorder':myorder})
