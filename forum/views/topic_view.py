from django.views.generic import ListView

from ..models import Reply, Topic


class TopicView(ListView):
    model = Reply
    template_name = 'forum/topic.html'
    context_object_name = 'reply_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Reply.objects.filter(
            topic__slug=self.kwargs['slug_topic'],
            topic__category__slug=self.kwargs['slug_subcategory'],
            topic__category__parent__slug=self.kwargs['slug_category'],)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic = Topic.objects.get(
            slug=self.kwargs['slug_topic'],
            category__slug=self.kwargs['slug_subcategory'],
            category__parent__slug=self.kwargs['slug_category'])

        context['category'] = topic.category.parent
        context['subcategory'] = topic.category
        context['topic'] = topic
        return context
