from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish_date__year=year,publish_date__month=month,publish_date__day=day)
    return render(request, 'blog/post_detail.html',{'post': post})
