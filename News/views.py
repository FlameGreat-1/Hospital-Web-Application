from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import News


def hospital_news(request):
    news_items = News.objects.all()
    return render(request, 'news.html', {'news_items': news_items})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})



def get_latest_news(count=3):
    return News.objects.all().order_by('-publication_date')[:count]
