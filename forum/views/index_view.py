from django.views.generic import ListView

from ..models import Category


class IndexView(ListView):
    model = Category
    queryset = Category.objects.filter(parent__isnull=True)
    template_name = 'forum/index.html'
    context_object_name = 'category_list'
