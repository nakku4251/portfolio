from django.views import generic
from .models import Post


class PostList(generic.ListView):
    model = Post
    ordering = '-created_at'
