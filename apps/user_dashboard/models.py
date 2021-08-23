from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.
class  TypeProfile(models.Model):
    type = models.CharField(max_length=20)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserManager(models.Manager):
    def validator_reg(self,postData):
        errores = {}
        if not LETTER_REGEX.match(postData["fname"]) or len(postData['fname']) < 2:
            errores['fname'] = "El nombre debe contener solo letras y tener un minimo de 2 caracteres"
        if not LETTER_REGEX.match(postData["lname"]) or len(postData['lname']) < 2:
            errores['lname'] = "El apellido debe contener solo letras y tener un minimo de 2 caracteres"
        if not EMAIL_REGEX.match(postData['email']):     
            errores['email'] = "Email invalido"
        if len(postData["password"]) < 8:
            errores['password'] = "Contraseña debe tener minimo 8 caracteres"
        if postData["password"] != postData["confirm_password"]:
            errores["confirm_password"] = "Contraseña no coincide"
        if self.filter(email__iexact=postData["email"]).exists():
            errores["email"] = "Email ya existe, favor ingresar uno nuevo"
        return errores
    def validator_log(self,postData):
        errores = {}
        if not EMAIL_REGEX.match(postData['email_login']):     
            errores['email_login'] = "Email invalido"
        if len(postData["password_login"]) < 8:
            errores['password_login'] = "Contraseña debe tener minimo 8 caracteres"
        return errores
    def validator_update_info(self,postData):
        errores = {}
        if not LETTER_REGEX.match(postData["fname"]) or len(postData['fname']) < 2:
            errores['fname'] = "El nombre debe contener solo letras y tener un minimo de 2 caracteres"
        if not LETTER_REGEX.match(postData["lname"]) or len(postData['lname']) < 2:
            errores['lname'] = "El apellido debe contener solo letras y tener un minimo de 2 caracteres"
        if not EMAIL_REGEX.match(postData['email']):     
            errores['email'] = "Email invalido"
        if self.filter(email__iexact=postData["email"]).exists() and postData["email"] != User.objects.get(id=postData["idUser"]).email:
            errores["email"] = "Email ya existe, favor ingresar uno nuevo"
        return errores
    def validator_update_pass(self,postData):
        errores = {}
        if len(postData["password"]) < 8:
            errores['password'] = "Contraseña debe tener minimo 8 caracteres"
        if postData["password"] != postData["confirm_password"]:
            errores["confirm_password"] = "Contraseña no coincide"
        return errores

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=255)
    profile = models.ForeignKey(TypeProfile, related_name='profiles_user',on_delete=models.CASCADE)
    desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class  MessageManager(models.Manager):
    def validate_messages(self,postData):
        errors = {}
        if postData["create_message"] == "":
            errors["create_message"] = "Publicacion vacia"
        return errors

class Message(models.Model):
    user = models.ForeignKey(User, related_name="users_messages",on_delete = models.CASCADE)
    foruser = models.ForeignKey(User, related_name="for_users_messages",on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class  CommentManager(models.Manager):
    def validate_comments(self,postData):
        errors = {}
        if postData["comment_message"] == "":
            errors["comment_message"] = "Comentario Vacio"
        return errors

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="users_comments",on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="messages_comments",on_delete = models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()