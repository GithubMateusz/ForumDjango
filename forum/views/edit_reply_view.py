from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from ..forms import ReplyForm
from ..models import Reply


@method_decorator(login_required, 'dispatch')
class EditReplyView(UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'forum/reply_form.html'

    def get_success_url(self):
        return reverse('topic', args=(
            self.object.topic.category.parent.slug,
            self.object.topic.category.slug,
            self.object.topic.slug))
