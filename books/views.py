from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Good, Restaurant, Category, Order, Menu, SignUpForm, FormCustoms
from django.db.models import Count
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate,login,logout
#导入包装的csrf请求，对跨站攻击脚本做处理
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict
from datetime import date, datetime
# Create your views here.
# def index(request):
# 	latest_good_list = Good.objects.all()
# 	output = ', '.join([p.name for p in latest_question_list])
# 	return HttpResponse(output)

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

@login_required(login_url="/login")  
def home(request):  
    return HttpResponse('Welcome, <a target="_blank" href="/·">logout</a>')  

@login_required(login_url="/login")
def index(request):
	user = request.user
	signUpForms = SignUpForm.objects.filter(state = 1).order_by('date')
	if  not signUpForms:
		signUpForms = SignUpForm(name = "订餐", state = 1)
		signUpForms.save()
	
	hasSignUp = FormCustoms.objects.filter(custom = user.custom).filter(sign_up_form = signUpForms[0])
	
	if not hasSignUp:
		template = loader.get_template('books/signup.html')
		context = RequestContext(request, {
			'signUpForms':signUpForms,
			'latestSignUpForm':signUpForms[0],
			'user':user,
			'hasSignUp':hasSignUp,
			})
		return HttpResponse(template.render(context))
	else:
		order = Order.objects.latest('date')
		if order.state != 1:
			return HttpResponse("<span style=\"color:red;\">饿了吗，管理还未制定店铺！</span>")
		goods = Menu.objects.filter(order = order.id).values('good').distinct()
		menus = Menu.objects.filter(order = order.id)
		goods_menus = {}
		len_set = {}
		user = request.user
		
		for good in goods:
			key = Good.objects.get(id = good['good']).name
			last_key = key
			menus = Menu.objects.filter(order = order.id).filter(good = good['good'])
			goods_menus[key] = {}
			goods_menus[key]['size'] = len(menus)
			goods_menus[key]['menus'] = menus
			

		_restaurant = Restaurant.objects.get(pk = order.restaurant.id)
		#goods = _restaurant.good_set.order_by('-category')
		#categorys_goods = Good.objects.filter(restaurant = _restaurant).annotate(dcount = Count('category'))
		#categorys = Good.objects.filter(restaurant = _restaurant.id).values("category").distinct()
		categorys = Good.objects.filter(restaurant = _restaurant).values('category').distinct()
		categorys_goods = {}
		
		for _category in categorys:
			key = Category.objects.get(id = _category['category']).name
			categorys_goods[key] = Good.objects.filter(restaurant = _restaurant).filter(category = _category['category'])
			

		restaurant_list = Restaurant.objects.all()
		template = loader.get_template('books/today_restaurant.html')
		context = RequestContext(request, {
			'restaurant': _restaurant,
			'order':order,
			'good_menus':menus,
			'categorys_goods':categorys_goods,
			'goods_menus':goods_menus,
			'user':user,
			})
		return HttpResponse(template.render(context))
		

@login_required(login_url="/login")
def signup(request):
	signUpForms = SignUpForm.objects.filter(state = 1).order_by('date')
	if  not signUpForms:
		signUpForms = SignUpForm(name = "订餐", state = 1)
		signUpForms.save()
	
	template = loader.get_template('books/signup.html')
	user = request.user
	hasSignUp = FormCustoms.objects.filter(custom = user.custom)
	context = RequestContext(request, {
		'signUpForms':signUpForms,
		'latestSignUpForm':signUpForms[0],
		'user':user,
		'hasSignUp':hasSignUp,
		})
	return HttpResponse(template.render(context))

@login_required(login_url="/login")
def custom_signup(request):
	user = request.user
	signUpForms = SignUpForm.objects.filter(state = 1)
	if  not signUpForms:
		signUpForms = SignUpForm(name = "订餐", state = 1)
		signUpForms.save()
	formCustom = FormCustoms.objects.filter(sign_up_form = signUpForms[0]).filter(custom = user.custom)
	
	if not formCustom:
		formCustom = FormCustoms(sign_up_form = signUpForms[0], custom = user.custom)
		formCustom.save()
	return index(request)
@login_required(login_url="/login")
@csrf_exempt
def obtain_signup_list(request):
	
	user = request.user
	if not user.is_staff:
		return HttpResponse("<span style=\"color:red;\">你无权访问此页面，你可以去<a href=\"../\">首页</a>看看</span>")
	form = SignUpForm.objects.latest('date')
	if  not form:
		form = SignUpForm(name = "订餐", state = 1)
		form.save()
	formCustoms = FormCustoms.objects.filter(sign_up_form = form)
	jsonStr = "["
	for formCustom in formCustoms:
		jsonStr += "{\"form_custom_id\":\"" + str(formCustom.id) + "\", \"form_name\":\"" + str(formCustom.custom.user.last_name + formCustom.custom.user.first_name) + "\"},"
	if len(jsonStr) > 1:
		jsonStr = jsonStr[:-1]
	jsonStr += "]"

	print(jsonStr)
	return HttpResponse(json.dumps(jsonStr))

@login_required(login_url="/login")
@csrf_exempt
def cancel_signup(request):
	print("cancel_signup")
	formCustomId =request.POST.get("form_custom_id",None)
	print("form_custom_id:" + formCustomId)
	if formCustomId:
		formCustom = FormCustoms.objects.get(id = formCustomId)
		formCustom.delete()
	return HttpResponse(json.dumps({"msg":"成功删除！"}))


@login_required(login_url="/login")
def select(request):
	user = request.user
	if not user.is_staff :
		return HttpResponse("<span style=\"color:red;\">你无权访问此页面，你可以去<a href=\"../\">首页</a>看看</span>")
	restaurant_list = Restaurant.objects.all()
	template = loader.get_template('books/select.html')
	
	context = RequestContext(request, {
		'restaurant_list': restaurant_list,
		'user':user,
    })
	return HttpResponse(template.render(context))

@login_required(login_url="/login")
@csrf_exempt
def obtain_opened_orders(request):
	user = request.user
	if not user.is_staff:
		return HttpResponse("<span style=\"color:red;\">你无权访问此页面，你可以去<a href=\"../\">首页</a>看看</span>")
	openedOrders = Order.objects.filter(state = 1)
	jsonStr = "["
	for order in openedOrders:
		jsonStr += "{\"restaurant\":\"" + str(order.restaurant.name) + "\","
		jsonStr += "\"order_id\":\"" + str(order.id) + "\","
		jsonStr += "\"date\":\"" + order.date.strftime('%Y-%m-%d %H:%M:%S') + "\""
		jsonStr += "},"
	if len(jsonStr) > 1:
		jsonStr = jsonStr[:-1]
	jsonStr += "]"
	print(jsonStr)
	return HttpResponse(json.dumps(jsonStr))

@login_required(login_url="/login")
@csrf_exempt
def turn_off_order(request):
	order_id =request.POST.get("order_id",None)
	print("order_id:" + order_id)
	if order_id:
		Order.objects.filter(id = order_id).update(state = 2)

	return HttpResponse(json.dumps({"msg":"成功关闭！"}))


@login_required(login_url="/login")
@csrf_exempt
def new_order(request):
	print('new_order')
	user = request.user
	if not user.is_staff:
		return HttpResponse("<span style=\"color:red;\">你无权访问此页面，你可以去<a href=\"../\">首页</a>看看</span>")

	restaurantId = request.POST.get("restaurantId",None)
	restaurant = Restaurant.objects.get(id = restaurantId)
	name = request.POST.get("name",None)
	print(name + restaurantId)
	order = Order(name = name, restaurant = restaurant, date = datetime.now(), state = 1)
	order.save()
	print(order)
	return HttpResponse(json.dumps({"msg":"成功添加"}))

@login_required(login_url="/login")
@csrf_exempt
def add_menu(request):
	goodId=request.POST.get("goodId",None)
	orderId = request.POST.get("orderId", None)
	print(goodId + "|" + orderId)
	order = Order.objects.get(id = orderId)
	good = Good.objects.get(id = goodId)
	menu = Menu(order = order, good = good, custom = request.user.custom, remark = "", comment = "", score = 0)
	menu.save()
	return HttpResponse(json.dumps({"msg":"成功添加到菜单"}))

@login_required(login_url="/login")
@csrf_exempt
def del_menu(request):
	menuIds = request.POST.get("menuIds",None)
	data_string = json.dumps(menuIds)
	menus = json.loads(data_string)
	for menu in eval(menus):
		print("del " + menu)
		menu = Menu.objects.get(id = menu)
		name = menu.good.name
		menu.delete()
	return HttpResponse(json.dumps({"msg":"成功删除！"}))

@login_required(login_url="/login")
@csrf_exempt
def update_menus(request):
	menuIds = request.POST.get("menuIds",None)
	remark = request.POST.get("remark",None)
	data_string = json.dumps(menuIds)
	menus = json.loads(data_string)
	for menu in eval(menus):
		print("update_menu " + menu)
		Menu.objects.filter(id = menu).update(remark = str(remark))
	return HttpResponse(json.dumps({"msg":"成功删除！"}))

@login_required(login_url="/login")
@csrf_exempt
def update_menu(request):
	menuId = request.POST.get("menuId",None)
	remark = request.POST.get("remark",None)
	comment = request.POST.get("comment", None)
	if remark:
		Menu.objects.filter(id = menuId).update(remark = str(remark))	

	if comment:
		Menu.objects.filter(id = menuId).update(comment = str(comment))	
	return HttpResponse(json.dumps({"msg":"成功删除！"}))


@login_required(login_url="/login")
@csrf_exempt
def get_own_menu(request):
	user = request.user
	menus = Menu.objects.filter(custom = user.custom)
	return HttpResponse(json.dumps({"msg":"获取成功！"}))


@login_required(login_url="/login")
@csrf_exempt
def load_own_order_detail(request):

	orderId = request.POST.get("orderId",None)
	user = request.user
	order = Order.objects.get(id = orderId)
	goods = Menu.objects.filter(order = order.id).filter(custom = user.custom).values('good').distinct()
	menus = Menu.objects.filter(order = order.id)
	
	goods_menus = {}
	
	if len(goods) == 0:
			return HttpResponse(json.dumps("[]"))
	jsonStr = "["
	for good in goods:
		jsonStr += "{"

		jsonStr += "\"key\": \"" + Good.objects.get(id = good['good']).name + "\""

		#key = Good.objects.get(id = good['good']).name
		good_menus = Menu.objects.filter(order = order.id).filter(good = good['good']).filter(custom = user.custom)
		
		jsonStr += ", \"size\":" + str(len(good_menus))
		jsonStr += ", \"good_total_price\":" + str(len(good_menus) * good_menus[0].good.price)
		jsonStr += ",  \"menus\":" + "["
		#tmp = model_to_dict(good_menus, fields=[], exclude=[])
		
		for menu in good_menus:
			jsonStr += "{"
			jsonStr += "\"menu\":" + json.dumps(model_to_dict(menu))
			jsonStr += ",\"order\":" + json.dumps(model_to_dict(menu.order), cls = CJsonEncoder)
			jsonStr += ",\"user_name\":" + "\"" + menu.custom.user.last_name + menu.custom.user.first_name + "\""
			jsonStr += "},"
		print("good_menus")
		jsonStr = jsonStr[:-1]
		jsonStr += "]"
		jsonStr += "},"

	if len(jsonStr) > 1:
		jsonStr = jsonStr[:-1]
	jsonStr += "]"
	print(jsonStr)
	return HttpResponse(json.dumps(jsonStr))

@login_required(login_url="/login")
@csrf_exempt
def load_order_detail(request):

	orderId = request.POST.get("orderId",None)

	order = Order.objects.get(id = orderId)
	goods = Menu.objects.filter(order = order.id).values('good').distinct()
	menus = Menu.objects.filter(order = order.id)
	
	goods_menus = {}
	
	jsonStr = "["
	for good in goods:
		jsonStr += "{"

		jsonStr += "\"key\": \"" + Good.objects.get(id = good['good']).name + "\""

		#key = Good.objects.get(id = good['good']).name
		good_menus = Menu.objects.filter(order = order.id).filter(good = good['good']).order_by('custom')

		jsonStr += ", \"size\":" + str(len(good_menus))
		jsonStr += ", \"good_total_price\":" + str(len(good_menus) * good_menus[0].good.price)
		jsonStr += ",  \"menus\":" + "["
		#tmp = model_to_dict(good_menus, fields=[], exclude=[])

		for menu in good_menus:

			jsonStr += "{"
			jsonStr += "\"menu\":" + json.dumps(model_to_dict(menu))
			jsonStr += ",\"order\":" + json.dumps(model_to_dict(menu.order), cls = CJsonEncoder)
			jsonStr += ",\"user_name\":" + "\"" + menu.custom.user.last_name + menu.custom.user.first_name + "\""
			jsonStr += "},"
		
		jsonStr = jsonStr[:-1]
		jsonStr += "]"
		jsonStr += "},"
	if len(jsonStr) > 1:
		jsonStr = jsonStr[:-1]
	jsonStr += "]"

	return HttpResponse(json.dumps(jsonStr))

@login_required(login_url="/login")
def restaurant(request, restaurant_id):
	_restaurant = Restaurant.objects.get(pk = restaurant_id)
	#goods = _restaurant.good_set.order_by('-category')
	#categorys_goods = Good.objects.filter(restaurant = _restaurant).annotate(dcount = Count('category'))
	#categorys = Good.objects.filter(restaurant = _restaurant.id).values("category").distinct()
	categorys = Good.objects.filter(restaurant = _restaurant).values('category').distinct()
	categorys_goods = {}
	for _category in categorys:
		key = Category.objects.get(id = _category['category']).name
		categorys_goods[key] = Good.objects.filter(restaurant = _restaurant).filter(category = _category['category'])
	user = request.user
	return render(request, 'books/restaurant.html', {'restaurant': _restaurant, "categorys_goods": categorys_goods,'user':user})

@login_required(login_url="/login")
def good(request, good_id):
	print(good_id)
	good = Good.objects.get(id = good_id)
	menus = Menu.objects.filter(good = good)
	print(menus)
	user = request.user
	return render(request, 'books/good.html', {"good": good, 'user':user,"menus":menus})

@login_required(login_url="/login")
def individual(request):
	user = request.user
	menus = Menu.objects.filter(custom = user.custom.id).order_by('order')
	return render(request, 'books/individual.html', { 'user':user, "menus":menus})

@login_required(login_url="/login")
def individual_in_restaurant(request, restaurant_id):
	user = request.user
	print(restaurant_id)
	restaurant = Restaurant.objects.get(id = restaurant_id)
	menus = Menu.objects.filter(custom = user.custom.id).filter(good__in = Good.objects.filter(restaurant = restaurant))
	print(menus)
	return render(request, 'books/individual.html', {'user':user, "menus":menus})


def login(request):
	print("---- login ----")
	return render(request, 'books/login.html')

@login_required(login_url="/login")
def password_change(request):
	print("---- password_change ----")
	return render(request, 'books/password_change_form.html')

def logout_view(request):
	print("---- logout ----")
	logout(request)
	return render(request, 'books/logout.html')
