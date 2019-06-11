from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import RegisterForm


class RegistrationView(CreateView):
    form_class = RegisterForm
    template_name = 'forum/registration.html'
    success_url = reverse_lazy('index')


