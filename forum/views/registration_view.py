from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'forum/registration.html'
    success_url = reverse_lazy('index')
