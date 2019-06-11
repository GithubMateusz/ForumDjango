from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dodaj_temat/<int:pk>/',
         views.AddTopicView.as_view(), name='add_topic'),

    path('dodaj_odpowiedz/<int:pk>/',
         views.AddAnswerView.as_view(), name='add_answer'),

    path('edytuj_temat/<int:pk>/',
         views.EditTopicView.as_view(), name='edit_topic'),

    path('edytuj_odpowiedz/<int:pk>/',
         views.EditAnswerView.as_view(), name='edit_answer'),


    path('<slug:category_slug>/'
         '<slug:subcategory_slug>/',
         views.CategoryView.as_view(), name='category'),

    path('<slug:category_slug>/'
         '<slug:subcategory_slug>/'
         '<slug:topic_slug>/',
         views.TopicView.as_view(), name='topic'),
]

