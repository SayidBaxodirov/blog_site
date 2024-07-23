from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post
from .forms import CommentForm


# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, publish_date__year=year,publish_date__month=month,publish_date__day=day)
    comments = post.comment_set.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',
                  {'post': post, "comment_form":comment_form, "comments":comments, "new_comment":new_comment})
