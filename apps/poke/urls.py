from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^pokes$',views.pokes),
	url(r'^main$', views.main),
	url(r'^logout$', views.logout),
	url(r'^users/(?P<user_id>[0-9]+)/delete$',views.destroy_user),
	url(r'^users/(?P<user_id>[0-9]+)/update$',views.update_user),
	url(r'^users/(?P<user_id>[0-9]+)/edit$',views.edit_user),
	url(r'^users/(?P<poker_id>[0-9]+)/poke/(?P<pokee_id>[0-9]+)$',views.poke_user),
	
	#edit/update user
	#delete user

	# url(r'^',views.main),

]