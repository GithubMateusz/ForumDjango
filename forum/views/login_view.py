from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'forum/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
