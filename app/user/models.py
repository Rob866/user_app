from django.db import models
from django.contrib.auth.models  import (
              AbstractBaseUser,
              BaseUserManager,User,
              PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self,username,nombre,apellido,email,password=None):
        email = self.normalize_email(email)
        user = self.model(
                      username=username,
                      nombre=nombre,
                      apellido=apellido,
                      email=email,
                      )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,nombre,apellido,email,password):
        user = self.create_user(
                    username=username,
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    password=password)
        user.is_staff= True
        user.is_superuser= True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser,PermissionsMixin):
     username = models.CharField(max_length=30,unique=True)
     nombre = models.CharField(max_length=100)
     apellido = models.CharField(max_length=100)
     email = models.EmailField(max_length=60,unique=True)

     USERNAME_FIELD  = 'username'
     REQUIRED_FIELDS = ['nombre','apellido','email']

     objects = UserManager()
     date_joined  =  models.DateTimeField(verbose_name="Fecha de ingreso",auto_now_add=False)
     last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
     is_active    =  models.BooleanField(verbose_name="¿Esta Activo?",default=True)
     is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)

     def  __str__(self):
         return f'{self.nombre}'
