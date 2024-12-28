from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
import json
from pathlib import Path

from .models import Category, Topic, Article
from .services.ai_service import AIService
from .forms import TopicForm

def home(request):
    topics_count = Topic.objects.count()
    articles_count = Article.objects.count()
    return render(request, 'core/home.html', {
        'topics_count': topics_count,
        'articles_count': articles_count,
    })

def topic_list(request):
    topics = Topic.objects.select_related('category').all()
    return render(request, 'core/topics/list.html', {'topics': topics})

def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('core:topic_list')
    else:
        form = TopicForm()
    
    return render(request, 'core/topics/create.html', {'form': form})

def topic_generate(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        count = int(request.POST.get('count', 3))
        
        category = get_object_or_404(Category, id=category_id)
        ai_service = AIService()
        
        topic_ideas = ai_service.generate_topic_ideas(category.name, count)
        
        # Save generated topics
        for idea in topic_ideas:
            Topic.objects.create(
                category=category,
                title=idea['title'],
                description=idea['description'],
                target_word_count=idea['target_word_count']
            )
        
        messages.success(request, f'Generated {len(topic_ideas)} new topics!')
        return redirect('core:topic_list')
    
    categories = Category.objects.all()
    return render(request, 'core/topics/generate.html', {'categories': categories})

def topic_detail(request, slug):
    topic = get_object_or_404(Topic.objects.select_related('category'), slug=slug)
    return render(request, 'core/topics/detail.html', {'topic': topic})

def article_list(request):
    articles = Article.objects.select_related('topic').all()
    return render(request, 'core/articles/list.html', {'articles': articles})

def article_generate(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        ai_service = AIService()
        content = ai_service.generate_article(topic)
        
        article = Article.objects.create(
            topic=topic,
            title=topic.title,
            content=content
        )
        
        topic.status = 'published'
        topic.save()
        
        messages.success(request, 'Article generated successfully!')
        return redirect('core:article_detail', slug=article.slug)
    
    return render(request, 'core/articles/generate.html', {'topic': topic})

def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related('topic'), slug=slug)
    return render(request, 'core/articles/detail.html', {'article': article})

def reset_database(request):
    if request.method == 'POST':
        # Delete all data
        Article.objects.all().delete()
        Topic.objects.all().delete()
        Category.objects.all().delete()
        messages.success(request, 'Database reset successfully!')
        return redirect('core:home')
    return render(request, 'core/db/reset.html')

def seed_database(request):
    if request.method == 'POST':
        # Load seed data from JSON
        seed_path = Path(settings.BASE_DIR) / 'topics.json'
        with open(seed_path) as f:
            seed_data = json.load(f)
        
        # Seed categories
        for cat_data in seed_data['categories']:
            Category.objects.create(**cat_data)
        
        # Seed topics
        for topic_data in seed_data['topics']:
            Topic.objects.create(**topic_data)
        
        messages.success(request, 'Database seeded successfully!')
        return redirect('core:home')
    return render(request, 'core/db/seed.html') 