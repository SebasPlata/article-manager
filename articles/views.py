from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "article_template.html"
    context_object_name = "articles"
    ordering = ["-id"]

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"

class ArticleCreateView(CreateView):
    model = Article
    fields = ["title", "content"]
    template_name = "article_form.html"
    success_url = reverse_lazy("articles:list")

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ["title", "content"]
    template_name = "article_form.html"
    success_url = reverse_lazy("articles:list")

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_confirm_delete.html"
    success_url = reverse_lazy("articles:list")