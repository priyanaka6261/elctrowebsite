from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField(max_length=100)
	mobile=models.PositiveIntegerField(max_length=100)
	address=models.TextField(max_length=100)
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to="profile_pic/",default="")
	usertype=models.CharField(max_length=100,default="buyer")

	def __str__(self):
		return(self.fname)
class Product(models.Model):
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	choice1=(
		("Laptop","Laptop"),
		("Acsessories","Acsessories"),
		("camera","camera"),
	)
	product_category=models.CharField(max_length=100,choices=choice1)
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to="product_image")
	def __str__(self):
		return self.seller.fname+" - "+self.product_name	
class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	product_price=models.PositiveIntegerField()
	product_qty=models.PositiveIntegerField(default=1)
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)

	


