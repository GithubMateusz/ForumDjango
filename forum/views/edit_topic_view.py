from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView

from forum.forms import TopicForm, AnswerForm
from forum.models import Topic


class EditTopicView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['reply'] = AnswerForm(
                self.request.POST,
                instance=self.object.answers.first())
        else:
            context['reply'] = AnswerForm(instance=self.object.answers.first())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        answer_form = AnswerForm(self.request.POST, instance=self.object.answers.first())
        if form.is_valid() and answer_form.is_valid():
            self.form_valid(form, answer_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, answer=answer_form))

    def form_valid(self, form, answer_form):
        self.object = form.save(commit=False)
        reply = answer_form.save(commit=False)
        reply.save()

    def get_success_url(self):
        return reverse('topic', args=[
            self.object.category.parent.slug,
            self.object.category.slug,
            self.object.slug])
