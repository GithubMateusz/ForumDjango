from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView

from ..forms import AnswerForm
from ..models import Answer



class EditAnswerView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'forum/answer_form.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('topic', args=(
            self.object.topic.category.parent.slug,
            self.object.topic.category.slug,
            self.object.topic.slug))
