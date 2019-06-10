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
            category__slug=self.kwargs['slug_subcategory'],
            category__parent__slug=self.kwargs['slug_category'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(
            slug=self.kwargs['slug_subcategory'],
            parent__slug=self.kwargs['slug_category'])
        context['category'] = category
        return context
