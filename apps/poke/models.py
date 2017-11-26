from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email


class UserManager(models.Manager):
	def user_validator(self,postData):
		errors = {}
		if len(postData['name']) < 2:
			errors['name'] = "Name should be 2 or more characters"
		if len(postData['alias']) < 1:
			errors['alias'] = "Alias should be 1 or more characters"
		if len(postData['email']) < 5:
			errors['email'] = "Please enter a valid email address"
		try:
			validate_email(postData['email'])
		except:
			errors['email_v'] = "Come on now.. that is not an email address..."
		if len(postData['password']) < 8:
			errors['password_length'] = "Password must be at least 8 characters "
		if postData['password'] != postData['password_confirm']:
			errors['password_match'] = "Password and Confirm PW must match"
		if postData['date_of_birth'] == "":
			errors['date_of_birth'] = "Please enter your date of birth"
		try:
			existing_user = User.objects.get(email=postData['email'])
			errors['email_exists'] = "There is already an account with this email"		
		except :
			pass

		try:
			existing_user = User.objects.get(alias=postData['alias'])
			errors['alias_exists'] = "There is already an account with this alias"
		except :
			pass
		return errors

	def update_user_validator(self, postData, user_id):
		
		errors = {}
		if len(postData['name']) < 2:
			errors['name'] = "Name should be 2 or more characters"
		if len(postData['email']) < 5:
			errors['email'] = "Please enter a valid email address"

		
		if len(postData['password']) > 0:	
			if len(postData['password']) < 8:
				errors['password_length'] = "Password must be at least 8 characters "
		if postData['password'] != postData['password_confirm']:
			errors['password_match'] = "Password and Confirm PW must match"
		if postData['date_of_birth'] == "":
			errors['date_of_birth'] = "Please enter your date of birth"
		try:
			existing_user = User.objects.get(email=postData['email'])
			if str(existing_user.id) != str(user_id):
				errors['email_exists'] = "There is already an account with this email"	

		except :
			pass
		

	
		return errors






class User(models.Model):
    name = models.CharField(max_length=255, blank=False)
    alias = models.CharField(max_length=255, blank=False, unique=True)
    email = models.CharField(max_length=255, blank=False, unique=True)
    hashed_password = models.CharField(max_length=72, blank=False)
    date_of_birth = models.DateField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __unicode__(self):
    	return  self.name + " " + self.alias + " " + self.email

	def __str__(self):
		return  self.name + " " + self.alias + " " + self.email

class Poke(models.Model):
	poker = models.ForeignKey(User, related_name='poker', blank=False, on_delete=models.CASCADE)
	pokee = models.ForeignKey(User, related_name='pokee', blank=False, on_delete=models.CASCADE)

	def __unicode__(self):
		return  self.poker + " poked: " + self.pokee 

	def __str__(self):
		return  self.poker + " poked: " + self.pokee 



		