
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('login/',views.login.as_view(),name='login'),
   path('signup/',views.signup.as_view(),name='signup'),
   path('profilet/',views.profilet.as_view(),name="profilet"),
   path('profiles/',views.profiles.as_view(),name="profiles"),
   path('logout/',views.logout_view,name="logout_view"),
   
   
   
   
    path('addquestionset/',views.addquestionset.as_view(),name="addquestionset"),
     path('',views.index.as_view(),name="index"),
     path("exam/<int:pk>",views.exam.as_view(),name="exam"),
      path('myquestionset/',views.view_myqestionsset.as_view(),name="myquestionset"),
       path('myexams/',views.view_myexams,name="myexams"),
     path("editquestionset/<int:pk>",views.edite_myquestionset.as_view(),name="edit_questionset"),
     
]
