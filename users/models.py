from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from organization.models import Organization



class MyAccountManager(BaseUserManager):

	def create_user(self, email, first_name, last_name, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not first_name:
			raise ValueError('Users must have a first name')
		if not last_name:
			raise ValueError('Users must have a last name')

		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, last_name ,password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			first_name=first_name,
			last_name=last_name
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	# username 				= models.CharField(max_length=30, unique=True)
	# TODO: for production do not allow null field
	first_name				= models.CharField(verbose_name="first_name", max_length=40)
	last_name 				= models.CharField(verbose_name="last_name", max_length=40)
	full_name 				= models.CharField(verbose_name="full_name", max_length=80)
	# 1 Employee has 1 Organization, but 1 Organization has many employees
	organization			= models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["first_name", "last_name",]

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissions
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True