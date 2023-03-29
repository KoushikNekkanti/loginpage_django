from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('contact/',views.contact,name='contact'),
    path('signout/',views.signout,name='signout'),
    path('forget/',views.forget,name='forget'),
    path('dash/',views.dash,name='dash'),
    path('todo/',views.todo,name='todo'),
    path('track/',views.track,name='track'),
    path('todo/add_todo/',views.add_todo,name='add_todo'),
    path('todo/delete_todo/<int:todo_id>',views.delete_todo,name='delete_todo'),
    path('todo/deleteall/',views.deleteall,name='deleteall'),
    path('square_run/',views.square_run,name='square_run'),
    path('notes/add_notes/',views.add_notes,name='add_notes'),
    path('notes/',views.notes,name='notes'),
    path('notes/delete_notes/<int:notes_id>',views.delete_notes,name='delete_notes'),
    path('notes/edit_notes/<str:notes_text>/<int:notes_id>',views.edit_notes,name='edit_notes'),
     path('notes/edit_notes/<str:notes_text>//<int:notes_id>/',views.edit_notes,name='edit_notes'),
      path('notes/edit_notes/<str:notes_text>///<int:notes_id>',views.edit_notes,name='edit_notes'),
    path('notes/edit_notes/<str:notes_text>/add_notes/',views.edit_notes_after),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
]