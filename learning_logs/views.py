from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    """Página principal do learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona novo assunto"""
    if request.method != 'POST':
        # Nenhum dado submetido, cria um form em branco
        form = TopicForm()
    else:
        # Dados submetidos processam os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
        
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Acrescenta nova entrada para o assunto"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Nenhum dado submetido, cria formulário em branco
        form = EntryForm()
    else:
        # Dados de POST, processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
            
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada preexistene"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #Requisição inicial preenche previamente o form com a entrada atual
        form = EntryForm(instance=entry)

    else:
        #Dados submetidos - processamento de dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
