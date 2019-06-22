from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import Select
from mptt.forms import TreeNodeChoiceField

from .models import Topic, Answer, Category


class DisabledChoiceWidget(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disabled_category = []

    @property
    def disabled_category(self):
        return self._disabled_category

    @disabled_category.setter
    def disabled_category(self, other):
        self._disabled_category = other

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        context = super().create_option(
            name, value, label, selected, index, subindex, attrs)
        if value in self.disabled_category:
            context['attrs']['disabled'] = 'disabled'
        return context


class AdminTopicForm(forms.ModelForm):
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        widget=DisabledChoiceWidget,
        required=False
    )

    class Meta:
        model = Topic
        exclude = ('created', 'latest_answer_date', 'latest_answer_author')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        disabled_category = Category.objects.filter(
            parent__isnull=True).values_list('id', flat=True)
        self.fields['category'].widget.disabled_category = disabled_category


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('name',)


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('body',)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = get_user_model()
        fields = ("username", "email", )
