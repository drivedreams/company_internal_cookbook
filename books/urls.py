from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^restaurant_(?P<restaurant_id>[0-9]+)/$', views.restaurant, name='restaurant'),
    url(r'^good_(?P<good_id>[0-9]+)/$', views.good, name='good'),
    url(r'^select$', views.select, name='select'),
    url(r'^home$', views.home, name='home'),
    url(r'^individual$', views.individual, name='individual'),
    url(r'^individual_in_restaurant_(?P<restaurant_id>[0-9]+)$', views.individual_in_restaurant, name='individual_in_restaurant'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^password_change', 'django.contrib.auth.views.password_change', name='password_change'),
	url(r'^logout$', views.logout_view, name = 'logout'),
	url(r'^signup$', views.signup, name = 'signup'),
	url(r'^obtain_signup_list$', views.obtain_signup_list, name = 'obtain_signup_list'),
	url(r'^obtain_opened_orders$', views.obtain_opened_orders, name = 'obtain_opened_orders'),
	url(r'^add_menu$', views.add_menu, name = 'add_menu'),
	url(r'^del_menu$', views.del_menu, name = 'del_menu'),
	url(r'^update_menus$', views.update_menus, name = 'update_menus'),
	url(r'^update_menu$', views.update_menu, name = 'update_menu'),
	url(r'^load_order_detail$', views.load_order_detail, name = 'load_order_detail'),
	url(r'^load_own_order_detail$', views.load_own_order_detail, name = 'load_own_order_detail'),
	url(r'^custom_signup$', views.custom_signup, name = 'custom_signup'),
	url(r'^cancel_signup$', views.cancel_signup, name = 'cancel_signup'),
	url(r'^turn_off_order$', views.turn_off_order, name = 'turn_off_order'),
	url(r'^new_order$', views.new_order, name= 'new_order')

]