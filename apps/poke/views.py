from django.shortcuts import render, HttpResponse, redirect
from .models import User, Poke
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import datetime

# from .. import bcrypt
# Create your views here.

def main(request):
	# response = "placeholder for main"
	# context = {'users': User.objects.all()}
 	# return render(request, 'semi_restful_users/index.html', context)
 	try:
 		user_id = request.session['user_id']
 		user = User.objects.all().get(id=user_id)
 		return redirect(pokes)
 	except:
 		request.session['user_id'] = ""
 	
 	# request.session['users'] = User.objects.all().first()
 	return render(request, 'poke/main.html')

def pokes(request):
	# response = "placeholder for pokes"
	try:
		context = {}
		display_users = []
		user_id = request.session['user_id']
		user = User.objects.all().get(id=user_id)
		users = User.objects.all()
		pokers = []
		number_of_pokers = 0
		for usr in users:
			if str(usr.id) != str(user_id):
				print "checking for pokers"
				times_poked = Poke.objects.filter(pokee=user_id, poker=usr.id).count()
				# times_poked = 3
				print times_poked
				if times_poked > 0:
					number_of_pokers += 1
					temp_poker = {}
					temp_poker['name'] = usr.name
					temp_poker['times_poked'] = times_poked
					pokers.append(temp_poker)

				u = {}
				u['id'] = usr.id
				u['name'] = usr.name
				u['alias'] = usr.alias
				u['email'] = usr.email
				print 'checking poke count'
				poke_count = Poke.objects.filter(pokee=usr.id).count()
				print poke_count
				u['poke_count'] = poke_count
				display_users.append(u)

		context['number_of_pokers'] = number_of_pokers
		context['user_name'] = user.name
		context['display_users'] = display_users
		# pokers = pokers.sort(key='times_poked', reverse=True)
		# context['pokers'] = pokers.sort(key='times_poked', reverse=True)
		context['pokers'] = sorted(pokers, key=lambda k: k['times_poked'], reverse=True)
		print 'worked so far...'
		print pokers
		return render(request, 'poke/pokes.html', context)

	except:
		request.session['user_id'] = ""
		return redirect(main)
	
	# context = {'users': User.objects.all()}
 	# return render(request, 'semi_restful_users/index.html', context)
 	

def login(request):
	try:
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.all().get(email=email)
		request.session['user_id'] = user.id
		hashed_pw = user.hashed_password
		# print hashed_pw

		if check_password(password, hashed_pw):
			print "login success"
			return redirect(pokes)
		else:
			print "login failed"
			request.session['user_id'] = ""
			return redirect(main)


	except:
		return redirect(main)
		
	# response = "placeholder for pokes"
	# context = {'users': User.objects.all()}
 	# return render(request, 'semi_restful_users/index.html', context)
 	

def logout(request):
	request.session['user_id'] = ""
	return redirect(main)

def register(request):
	errors = User.objects.user_validator(request.POST)
	# messages = {}
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error)
			print messages
		return redirect(main)
	else:

	 	print "in register"
	 	try:
		 	name = request.POST['name']
		 	# print name
		 	alias = request.POST['alias']
		 	# print alias
		 	email = request.POST['email']
		 	# print email
		 	password = request.POST['password']
		 	# print password
		 	date_of_birth = request.POST['date_of_birth']
		 	print "Entered birth date: " + date_of_birth
		 	hashed_password = make_password(password, hasher='bcrypt_sha256')
		 	
		 	# print hashed_password
		 	date_of_birth = datetime.datetime.now().date()
		 	# print "Today's date: " + date_of_birth
		 	print "attempting to create user..."
		 	user = User.objects.create(name=name, alias=alias, email=email, hashed_password=hashed_password, date_of_birth=date_of_birth)
		 	
		 	print "user created"
		 	# print user.name
		 	request.session['user_id'] = user.id

		 	# request.session['users'] = User.objects.all()

		 	return redirect(pokes)		
	 	except:
	 		request.session['user_id'] = ""
	 		return redirect(main)	


def destroy_user(request, user_id):

	try:
		if str(request.session['user_id']) == str(user_id):
			user = User.objects.all().get(id=user_id)
			user.delete()
			request.session['user_id'] = ""
			return redirect(main)
		else:
			return redirect(main)
	except :
		return redirect(main)

def update_user(request, user_id):
	errors = User.objects.update_user_validator(request.POST, user_id)
	# messages = {}
	if len(errors):
		print "errors were found!"
		for tag, error in errors.iteritems():
			messages.error(request, error)
			print messages
		return redirect(main)
	else:
		try:
			print "Attempting to update user"

			if str(request.session['user_id']) == str(user_id):
				print "User is logged in"
				
				
				name = request.POST['name']
				print name
				# alias = request.POST['alias']
				# print alias
				email = request.POST['email']
				# print email
				new_password = request.POST['password']
				# print new_password
				date_of_birth = request.POST['date_of_birth']
				# print date_of_birth
				user = User.objects.get(id=user_id)
				# print user.date_of_birth
				user.name = name
				# user.alias = alias
				user.email = email
				user.date_of_birth = date_of_birth
				if new_password != "":
					hashed_password = make_password(new_password, hasher='bcrypt_sha256')
					user.hashed_password = hashed_password
				user.save()

				
				
				# print user.date_of_birth
				
				print "User has been updated!"
				return redirect(main)
			else:
				return redirect(main)
		except:
			return redirect(main)

def edit_user(request, user_id):
	print "In Edit"
	try:
		if str(request.session['user_id']) == str(user_id):
			print "User is logged in"
			user = User.objects.all().get(id=user_id)
			context = {}
			context['name'] = user.name
			context['alias'] = user.alias
			context['email'] = user.email
			context['date_of_birth'] = user.date_of_birth
			return render(request, 'poke/user_edit.html', context)
		else:
			return redirect(main)


	except:
		return redirect(main)
		

def poke_user(request, poker_id, pokee_id):
	try:
		if str(request.session['user_id']) == str(poker_id):
			pokee = User.objects.get(id=pokee_id)
			poker = User.objects.get(id=poker_id)
			Poke.objects.create(poker=poker, pokee=pokee)

			
			
			return redirect(main)
		else:
			return redirect(main)
	except :
		return redirect(main)
	# response = "placeholder for pokes"
	# context = {'users': User.objects.all()}
 	# return render(request, 'semi_restful_users/index.html', context)
 	return redirect(pokes)