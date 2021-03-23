from django.shortcuts import render, get_object_or_404 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm
from taggit.models import Tag 

def post_list(request, tag_slug=None):  
    object_list = Post.published.all()  
    tag = None 

    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        object_list = object_list.filter(tags__in=[tag]) 

    paginator = Paginator(object_list, 3)  # 3 поста на каждой странице  
    page = request.GET.get('page')  
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages)  
    return render(request,  
	          'blog/post/list.html',  
		  {'page': page,  
		   'posts': posts,
           'tag': tag})
              
def post_detail(request, year, month, day, post):  
    post = get_object_or_404(Post, slug=post,  
				   status='published',  
				   publish__year=year,  
				   publish__month=month,  
				   publish__day=day)  
    # Список активных комментариев к этой записи  
    comments = post.comments.filter(active=True)  
    new_comment = None  
    if request.method == 'POST':  
        # Комментарий был опубликован
        comment_form = CommentForm(data=request.POST)  
        if comment_form.is_valid():  
            # Создайте объект Comment, но пока не сохраняйте в базу данных
            new_comment = comment_form.save(commit=False)  
            # Назначить текущий пост комментарию
            new_comment.post = post  
            # Сохранить комментарий в базе данных 
            new_comment.save()  
    else:  
        comment_form = CommentForm()  
    return render(request,  
		  'blog/post/detail.html',  
		  {'post': post,  
		  'comments': comments,  
		  'new_comment': new_comment,  
		  'comment_form': comment_form})
        
class PostListView(ListView):  
    queryset = Post.published.all()  
    context_object_name = 'posts'  
    paginate_by = 3  
    template_name = 'blog/post/list.html'