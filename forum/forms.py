from django import forms

from .models import Topic, Reply


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('body',)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name',)

