from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Topic, Answer


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = get_user_model()
        fields = ("username", "email", )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)

