from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('notes/',views.notes, name="notes"),
    path('delete_notes/<int:pk>',views.delete_notes, name="delete_notes"),
    path('notes_detail/<int:pk>',views.notes_detail.as_view(), name="notes_detail"),
    path('homework/',views.homework, name="homework"),
    path('homework_update/<int:pk>',views.homework_update, name="homework_update"),
    path('homework_delete/<int:pk>',views.delete_homework, name="homework_delete"),
    path('youtube/',views.youtube, name="youtube"),
    path('todo/',views.todo, name="todo"),
    path('todo_update/<int:pk>',views.todo_update, name="todo_update"),
    path('todo_delete/<int:pk>',views.todo_delete, name="todo_delete"),
    path('books/',views.books, name="books"),
    path('dictionary/',views.dictionary, name="dictionary"),
    path('wiki/',views.wiki, name="wiki"),
    path('conversion/',views.conversion, name="conversion"),
    path('about/',views.about, name="about"),
    
]
