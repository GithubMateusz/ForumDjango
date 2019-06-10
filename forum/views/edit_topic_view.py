from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from forum.forms import TopicForm, ReplyForm
from forum.models import Topic


@method_decorator(login_required, 'dispatch')
class EditTopicView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['reply'] = ReplyForm(
                self.request.POST,
                instance=self.object.reply.first())
        else:
            context['reply'] = ReplyForm(instance=self.object.reply.first())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        reply_form = ReplyForm(self.request.POST, instance=self.object.reply.first())
        if form.is_valid() and reply_form.is_valid():
            self.form_valid(form, reply_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, reply=reply_form))

    def form_valid(self, form, reply_form):
        self.object = form.save(commit=False)
        reply = reply_form.save(commit=False)
        reply.save()

    def get_success_url(self):
        return reverse('topic', args=[
            self.object.category.parent.slug,
            self.object.category.slug,
            self.object.slug])
