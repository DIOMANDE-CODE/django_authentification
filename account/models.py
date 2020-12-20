from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, name, company_name, phone, password=None):
        if not email:
            raise ValueError("Le champs email est obligatoire")
        if not first_name:
            raise ValueError("Veuillez indiquer votre prenom")
        if not name:
            raise ValueError("Veuillez donner votre nom")
        if not company_name:
            raise ValueError("Veuillez indiquer le nom de votre entreprise")
        if not phone:
            raise ValueError("Veuillez renseigner le numéro de téléphone")

        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            name=name,
            company_name=company_name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, name, company_name, phone, password=None):
        user=self.create_user(
            email=email,
            first_name=first_name,
            name=name,
            company_name=company_name,
            phone=phone,
            password=password 
        )
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name='Adresse Email', max_length=60, unique=True)
    first_name=models.CharField(verbose_name='Nom', max_length=200)
    name=models.CharField(verbose_name='Prenom', max_length=200)
    company_name=models.CharField(verbose_name='Nom de la compagnie', max_length=200, unique=True)
    phone=models.CharField(verbose_name='Numero de téléphone', max_length=20)
    date_joined=models.DateTimeField(auto_now_add=True, verbose_name="date de création")
    last_login=models.DateTimeField(auto_now_add=True, verbose_name='dernière connexion')
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
 
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['first_name','name','company_name','phone']

    objects=MyUserManager()

    def __str__(self):
        return self.company_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_labbel):
        return True