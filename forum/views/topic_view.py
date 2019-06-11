from django.views.generic import ListView

from ..models import Answer, Topic


class TopicView(ListView):
    model = Answer
    template_name = 'forum/topic.html'
    context_object_name = 'answers_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Answer.objects.filter(
            topic__slug=self.kwargs['topic_slug'],
            topic__category__slug=self.kwargs['subcategory_slug'],
            topic__category__parent__slug=self.kwargs['category_slug'],)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic = Topic.objects.get(
            slug=self.kwargs['topic_slug'],
            category__slug=self.kwargs['subcategory_slug'],
            category__parent__slug=self.kwargs['category_slug'])

        context['category'] = topic.category.parent
        context['subcategory'] = topic.category
        context['topic'] = topic
        return context
