from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
from django.core.paginator import Paginator
from django.db.models import Q  # Q object

# Create your views here.


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)  # body指模型的body字段 icontains指不区分大小写的包含
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    paginator = Paginator(article_list, 3)  # 3 means tree articles in every page
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # total_views
    article.total_views += 1
    article.save(update_fields=['total_views'])  # 指定更新字段，优化执行效率

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ]
                                     )

    # debug
    # print(article.body)

    context = {'article': article}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():  # is_valid()
            new_article = article_post_form.save(commit=False)  # save() commit
            # 指定id=1的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()  # save()
            return redirect('article:article_detail', id=new_article.id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        # Authentication
        if request.user != article.author:
            return HttpResponse('抱歉，您无权删除这篇文章。')
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    # print(id)
    article = ArticlePost.objects.get(id=id)
    # Authentication
    if request.user != article.author:
        return HttpResponse('抱歉，您无权修改这篇文章。')
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        print('here')
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = {
            'article': article,
            'article_post_form': article_post_form
        }
        return render(request, 'article/update.html', context)
