from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dodaj_temat/pk=<int:pk_category>/',
         views.AddTopicView.as_view(), name='add_topic'),

    path('dodaj_odpowiedz/pk=<int:pk_topic>/',
         views.AddReplyView.as_view(), name='add_reply'),

    path('<slug:slug_category>/'
         '<slug:slug_subcategory>/',
         views.CategoryView.as_view(), name='category'),

    path('<slug:slug_category>/'
         '<slug:slug_subcategory>/'
         '<slug:slug_topic>/',
         views.TopicView.as_view(), name='topic'),
]
