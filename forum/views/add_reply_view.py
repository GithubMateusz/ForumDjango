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
    template_name = 'forum/add_reply.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        topic = Topic.objects.get(
            pk=self.kwargs['pk_topic'])

        self.object = form.save(commit=False)
        self.object.topic = topic
        self.object.save()

        return HttpResponseRedirect(
            reverse('topic', args=(
                topic.category.parent.slug,
                topic.category.slug,
                topic.slug)))
