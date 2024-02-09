from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("results/", views.results, name="results"),
    path("upload/", views.upload, name="upload"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("signIn/", views.signIn, name="login"),
    path("train_model/", views.train_model, name="train_model"),
    path("logout_view/", views.logout_view, name="logout_view"),
]
