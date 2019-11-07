from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from ..forms import TopicForm, AnswerForm
from ..models import Topic, Category, Answer


class AddTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['reply'] = AnswerForm(self.request.POST)
        else:
            context['reply'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        answer_form = AnswerForm(self.request.POST, instance=Answer())
        if form.is_valid() and answer_form.is_valid():
            self.form_valid(form, answer_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, answer=answer_form))

    def form_valid(self, form, answer_form):
        form.instance.author = self.request.user
        answer_form.instance.author = self.request.user
        category = Category.objects.get(
            pk=self.kwargs['pk'])

        self.object = form.save(commit=False)
        self.object.category = category
        self.object.save()

        reply = answer_form.save(commit=False)
        reply.topic = self.object
        reply.save()

    def form_invalid(self, form, answer_form):
        return self.render_to_response(
            self.get_context_data(form=form, answer=answer_form)
        )

    def get_success_url(self):
        return reverse('category', args=[
            self.object.category.parent.slug,
            self.object.category.slug])
