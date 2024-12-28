from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
import json
from pathlib import Path
from django.core.serializers.json import DjangoJSONEncoder

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
        
        # Prepare topics data for the template
        topics_json = json.dumps(topic_ideas)
        
        return render(request, 'core/topics/review.html', {
            'category': category,
            'topics': topic_ideas,
            'topics_json': topics_json
        })
    
    categories = Category.objects.all()
    return render(request, 'core/topics/generate.html', {'categories': categories})

def topic_save(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        selected_indices = request.POST.getlist('selected_topics')
        topics_data = json.loads(request.POST.get('topics_data'))
        
        category = get_object_or_404(Category, id=category_id)
        
        # Save only selected topics
        saved_count = 0
        for index in selected_indices:
            topic_data = topics_data[int(index)]
            Topic.objects.create(
                category=category,
                title=topic_data['title'],
                description=topic_data['description']
            )
            saved_count += 1
        
        messages.success(request, f'Saved {saved_count} topics successfully!')
        return redirect('core:topic_list')
    
    return redirect('core:topic_generate')

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
        try:
            # Load seed data from JSON
            seed_path = Path(settings.BASE_DIR) / 'topics.json'
            with open(seed_path) as f:
                seed_data = json.load(f)
            
            # Create a dictionary to map old category IDs to new ones
            category_id_map = {}
            
            # Seed categories first and build the mapping
            for index, cat_data in enumerate(seed_data['categories'], 1):
                category = Category.objects.create(
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    description=cat_data['description']
                )
                # Map the position in the list (1-based) to the new category ID
                category_id_map[index] = category.id
            
            # Seed topics using the mapped category IDs
            for topic_data in seed_data['topics']:
                # Map the old category_id to the new one
                new_category_id = category_id_map[topic_data['category_id']]
                Topic.objects.create(
                    title=topic_data['title'],
                    description=topic_data['description'],
                    category_id=new_category_id
                )
            
            messages.success(request, 'Database seeded successfully!')
            return redirect('core:home')
            
        except Exception as e:
            messages.error(request, f'Error seeding database: {str(e)}')
            return redirect('core:home')
            
    return render(request, 'core/db/seed.html') 