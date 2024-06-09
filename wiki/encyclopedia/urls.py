from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Create_New_Page", views.create_new_page, name="create_new_page"),
    path("wiki/<str:url_name>", views.entry, name="entry"),
    path("Search", views.search, name="search"),
    path("Edit_Page/<str:url_name>", views.edit_page, name="edit_page"),
    path("Random_Page", views.random_page, name="random_page"),
]
