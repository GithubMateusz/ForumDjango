from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import CreateView

from ..forms import AnswerForm
from ..models import Answer, Topic


class AddAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'forum/answer_form.html'

    def get(self, request, *args, **kwargs):
        topic = Topic.objects.get(
            pk=self.kwargs['pk'])
        if topic.latest_answer_author == self.request.user:
            raise Http404("")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form))

    def form_valid(self, form):
        form.instance.author = self.request.user
        topic = Topic.objects.get(
            pk=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.topic = topic
        self.object.save()

    def get_success_url(self):
        return reverse('topic', args=(
            self.object.topic.category.parent.slug,
            self.object.topic.category.slug,
            self.object.topic.slug))


