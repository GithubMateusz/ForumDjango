from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from ..forms import ReplyForm
from ..models import Reply, Topic


@method_decorator(login_required, 'dispatch')
class AddReplyView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'forum/reply_form.html'

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


