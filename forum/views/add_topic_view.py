from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from ..forms import TopicForm, ReplyForm
from ..models import Topic, Category, Reply


@method_decorator(login_required, 'dispatch')
class AddTopicView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/add_topic.html'

    def get_context_data(self, **kwargs):
        context = super(AddTopicView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['reply'] = ReplyForm(self.request.POST)
        else:
            context['reply'] = ReplyForm()
        return context

    def form_valid(self, form):
        reply_form = ReplyForm(self.request.POST, instance=Reply())
        if reply_form.is_valid():
            form.instance.author = self.request.user
            reply_form.instance.author = self.request.user

            category = Category.objects.get(
                pk=self.kwargs['pk_category'])
            self.object = form.save(commit=False)
            self.object.category = category
            self.object.save()

            reply = reply_form.save(commit=False)
            reply.topic = self.object
            reply.save()
            if category.parent.parent:
                return HttpResponseRedirect(
                    reverse('category', args=(
                        category.parent.parent.slug,
                        category.parent.slug,
                        category.slug)))
            else:
                return HttpResponseRedirect(
                    reverse('category', args=(
                        category.parent.slug,
                        category.slug)))
        else:
            return self.form_invalid(form, reply_form)

    def form_invalid(self, form, reply_form):
        return self.render_to_response(
            self.get_context_data(form=form, reply=reply_form)
        )
