from django.views.generic import ListView
from django.db.models import Q

from ..models import Topic, Category


class CategoryView(ListView):
    model = Topic
    template_name = 'forum/category.html'
    object_list = 'topic_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):

        return Topic.objects.filter(
            ~Q(status='hidden'),
            category__slug=self.kwargs['subcategory_slug'],
            category__parent__slug=self.kwargs['category_slug'])\
            .order_by('-latest_answer_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(
            slug=self.kwargs['subcategory_slug'],
            parent__slug=self.kwargs['category_slug'])
        context['category'] = category
        return context
