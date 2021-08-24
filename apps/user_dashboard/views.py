from django.contrib import messages
from django.shortcuts import render,redirect,render_to_response
from django.db.models import Count
from django.http import JsonResponse
from .models import User, Message, TypeProfile, Comment
from datetime import datetime
import bcrypt
import locale
# Create your views here.
def index(request):
    return render(request, "index.html")

def signin(request):
    if request.method == "GET":
        if "id" in request.session:
            return redirect("/dashboard")
    return render(request, "login_registration.html")

def add_user(request):
    if request.method == "GET":
        if "id" in request.session and User.objects.get(id=request.session["id"]).profile.level == 9:
            return render(request, "add_new_user.html")
    return redirect("/")

def register_user(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        errors = User.objects.validator_reg(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)
        try:
            User.objects.get(id=1)
            usuario = User.objects.create(first_name=fname,last_name=lname,email=email,password=password_hs,profile=TypeProfile.objects.get(level=1))
        except:
            usuario = User.objects.create(first_name=fname,last_name=lname,email=email,password=password_hs,profile=TypeProfile.objects.get(level=9))
        return JsonResponse({"resultado": usuario.id })
    return redirect("/")

def login(request):
    if request.method == "POST":
        email = request.POST["email_login"]
        password = request.POST["password_login"]
        errors = User.objects.validator_log(request.POST)
        if len(errors) > 0:
            return JsonResponse(errors)   
        try:
            usuario = User.objects.get(email=email)
        except:
            errors = {
                "email_login" : "Email no existe favor registrese"
            }
            return JsonResponse(errors) 
        if bcrypt.checkpw(password.encode(), usuario.password.encode()):
            request.session["id"] = usuario.id
            return JsonResponse({"resultado": usuario.id })
        else:
            errors = {
                "password_login" : "Contraseña incorrecta"
            }
            return JsonResponse(errors)

def logout(request):
    if request.method == "GET":
        if "id" in request.session:
            del request.session['id']
        return redirect("/")

def dashboard(request):
    if request.method == "GET":
        if "id" in request.session:
            context = {
                "usuarios" : User.objects.all().order_by("id"),
                "perfil" : User.objects.get(id=request.session["id"]),
            }
            return render(request,"dashboard.html", context)
    return redirect("/")

def update_user(request,idUser):
    if request.method == "POST":
        if "id" in request.session:
            errors = User.objects.validator_update_info(request.POST)
            if len(errors) > 0:
                return JsonResponse(errors)
            try:
                user = User.objects.get(id=idUser)
            except:
                return redirect(f"/edit/{idUser}")
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            try:
                user.profile = TypeProfile.objects.get(id=request.POST["profile"]) 
            except:
                user.save()
        return JsonResponse({"resultado": user.id })

def update_pass(request,idUser):
    if request.method == "POST":
        if "id" in request.session:
            errors = User.objects.validator_update_pass(request.POST)
            if len(errors) > 0:
                return JsonResponse(errors)
            try:
                user = User.objects.get(id=idUser)
            except:
                return redirect(f"/edit/{idUser}")
            password_hs = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            user.password = password_hs
            user.save()
        return JsonResponse({"resultado": user.id })

def predestroy(request, idUser):
    if request.method == "GET":
        if "id" in request.session:
            try:
                user = User.objects.get(id=idUser)
            except:
                user = None
                return redirect("/dashboard")
            context={
                'name': f'{user.first_name} {user.last_name}',
                'email' : user.email,
                'id' : user.id,
            }
            return JsonResponse(context)
    return redirect("/")

def destroy(request,idUser):
    if request.method == "GET":
        if "id" in request.session and User.objects.get(id=request.session["id"]).profile.level == 9:
            try:
                user = User.objects.get(id=idUser)
            except:
                user = None
                return redirect("/dashboard")
            if user.id != 1:
                user.delete()
    return redirect("/dashboard")

def edit_user(request,idUser):
    if request.method == "GET":
        if "id" in request.session and User.objects.get(id=request.session["id"]).profile.level == 9:
            try:
                user = User.objects.get(id=idUser)
            except:
                user = None
                return redirect("/dashboard")
            context={
                "usuario" : user,
                "levels" : TypeProfile.objects.all()
            }
            return render(request, "edit_user.html", context)
    return redirect("/dashboard")

def edit_profile(request):
    if request.method == "GET":
        if "id" in request.session:
            try:
                user = User.objects.get(id=request.session["id"])
            except:
                user = None
                return redirect("/dashboard")
            context={
                "usuario" : user
            }
            return render(request, "profile.html", context)
    elif request.method == "POST":
        if "id" in request.session:
            try:
                user = User.objects.get(id=request.session["id"])
            except:
                user = None
                return redirect("/dashboard")
            user.desc = request.POST["description"]
            user.save()
    return redirect("/dashboard")

def show_user(request, idUser):
    if request.method == "GET":
        if "id" in request.session:
            try:
                user = User.objects.get(id=idUser)
            except:
                user = None
                return redirect("/dashboard")
            context={
                "usuario" : user,
                "message_users" : Message.objects.filter(foruser=user).order_by("-id"),
                "comments" : Comment.objects.all().order_by("id"),
            }
            return render(request, "user.html", context)

def create_message(request):
    if request.method == "POST":
        if "id" in request.session:
            errors = Message.objects.validate_messages(request.POST)
            if len(errors) > 0:
                return JsonResponse(errors)
            usuario = User.objects.get(id=request.session["id"])
            forUser = User.objects.get(id=request.POST["foruser"])
            mensaje = request.POST["create_message"]
            new_message = Message.objects.create(user=usuario,foruser=forUser,message=mensaje)
            data = {
                "id" : new_message.id,
                "message" : new_message.message,
                "first_name" : new_message.user.first_name,
                "last_name" : new_message.user.last_name,
                "created_at" : datetime.strftime(new_message.created_at, "%d de %B de %Y a las %H:%M")
            }
            return JsonResponse(data)
            #redirect(f"/show/{forUser.id}")
    return redirect("/")

def comment_message(request, idMessage):
    if request.method == "POST":
        if "id" in request.session:
            errors = Comment.objects.validate_comments(request.POST)
            if len(errors) > 0:
                errors["idMessage"] = idMessage
                return JsonResponse(errors)
            idusuario = request.session["id"]
            usuario = User.objects.get(id=idusuario)
            try:
                mensaje = Message.objects.get(id=idMessage)
            except:
                return JsonResponse({"errors": "No se puede comentar en esta publicacion"})
            comentario = request.POST["comment_message"]
            new_commentario = Comment.objects.create(user=usuario,message=mensaje,comment=comentario)
            data = {
                "id" : new_commentario.id,
                "idMessage" : new_commentario.message.id,
                "message" : new_commentario.message.message,
                "first_name" : new_commentario.user.first_name,
                "last_name" : new_commentario.user.last_name,
                "comment" : new_commentario.comment,
                "created_at" : datetime.strftime(new_commentario.created_at, "%d de %B de %Y a las %H:%M").lower()
            }
            return JsonResponse(data)
    return redirect("/")

def comment_delete(request,idComment):
    if request.method == "GET":
        if "id" in request.session:
            del_comment = Comment.objects.get(id=idComment)
            del_comment.delete()   
            return JsonResponse({"id" : idComment})
    return redirect("/")