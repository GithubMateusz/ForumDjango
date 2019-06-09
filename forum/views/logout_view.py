from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class LogoutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get(request, *args, **kwargs)
