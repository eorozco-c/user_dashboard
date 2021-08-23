from django.urls import  path
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('signin', views.signin,name="signin"),
    path('login',views.login, name="login"),
    path('logout',views.logout, name="logout"),
    path('register',views.register_user, name="register"),
    path('dashboard',views.dashboard, name="dashboard"),
    path('new',views.add_user, name="addUser"),
    path('edit',views.edit_profile, name="editProfile"),
    path('show/<int:idUser>',views.show_user,name="showUser"),
    path('edit/<int:idUser>',views.edit_user, name="editUser"),
    path('update/<int:idUser>',views.update_user, name="updateUser"),
    path('update_pass/<int:idUser>',views.update_pass, name="updatePass"),
    path('predestroy/<int:idUser>',views.predestroy, name="predestroy"),
    path('destroy/<int:idUser>',views.destroy, name="destroy"),
    path('create_message',views.create_message,name="createMessage"),
    path('comment_message/<int:idMessage>', views.comment_message, name="commentMessage"),
    path('comment_delete/<int:idComment>', views.comment_delete,name="deleteComment"),
]
