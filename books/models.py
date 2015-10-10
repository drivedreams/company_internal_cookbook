from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class Restaurant(models.Model):
	name = models.CharField(max_length=50)
	URL = models.CharField(max_length=200, default="")
	pic = models.ImageField(upload_to='upload/images/good_pic', default="")

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Good(models.Model):
	name = models.CharField(max_length=50)
	price = models.FloatField()
	description = models.CharField(max_length=200, null = True, blank= True)
	category = models.ForeignKey(Category)
	restaurant = models.ForeignKey(Restaurant)
	times = models.IntegerField(default = 0)
	score = models.IntegerField(default = 0)
	pic = models.ImageField(upload_to='upload/images/good_pic', default="")

	def __str__(self):
		return self.name + "|" + str(self.price) + "|" + self.restaurant.name + "|" + self.category.name + "|" + str(self.times)

class Department(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Custom(models.Model):
	user = models.OneToOneField(User, null=True)
	sex=models.CharField(verbose_name='性别',choices=(("M","男"),("F","女")),max_length=1)
	age = models.IntegerField()
	department = models.ForeignKey(Department)
	pic = models.ImageField(upload_to = 'upload/images/custom', blank=True, null=True)

	def __str__(self):
		return self.user.last_name + self.user.first_name + "|" + self.department.name

class Order(models.Model):
	name = models.CharField(max_length=50, default= "晚餐")
	date = models.DateTimeField(default="")
	restaurant = models.ForeignKey(Restaurant)
	state = models.IntegerField(verbose_name='订单状态', default = 1, choices=((1,"开启"),(2,"关闭")))

	def __str__(self):
		return self.name + "|" + self.date.strftime('%Y-%m-%d %H:%M:%S')

	def date_24(self):
		return self.date.strftime('%Y-%m-%d %H:%M:%S')

	def default(self, obj):
	    if isinstance(obj, datetime):
	        return obj.strftime('%Y-%m-%d %H:%M:%S')
	    elif isinstance(obj, date):
	        return obj.strftime('%Y-%m-%d')
	    else:
	        return json.JSONEncoder.default(self, obj)

class SignUpForm(models.Model):
	name = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now=True)
	order = models.ForeignKey(Order, null = True, blank=True)
	state = models.IntegerField(verbose_name='报名表状态', default = 1, choices=((1,"开启"),(2,"关闭")))
	
	def __str__(self):
		return self.name + "|" + self.date.strftime('%Y-%m-%d %H:%M:%S')

class FormCustoms(models.Model):
	sign_up_form = models.ForeignKey(SignUpForm)
	custom = models.ForeignKey(Custom)

	def __str__(self):
		return self.sign_up_form.name + "|" + self.custom.user.last_name + self.custom.user.first_name + "|" + self.sign_up_form.date.strftime('%Y-%m-%d %H:%M:%S')

class Menu(models.Model):
	order = models.ForeignKey(Order)
	good = models.ForeignKey(Good)
	custom = models.ForeignKey(Custom)
	remark = models.CharField(max_length=200, default="", blank=True)
	comment = models.CharField(max_length= 200, blank = True, default= "")
	score = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.order.name + "|" + self.good.name + "|" + self.custom.user.username
	def is_comment_null(self):
		if self.comment :
			return False
		else :
			return True
