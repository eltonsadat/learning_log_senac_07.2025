from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    """Página inicial do Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os tópicos criados"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um tópico e seus registros"""
    topic = Topic.objects.get(id=topic_id)

    #Garante que a anotação seja visível apenas para o dono
    if topic.owner != request.user:
        return render(request, '404.html', status=404)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo tópico"""
    if request.method != 'POST':
        #Nada foi enviado, retorna um formulário em branco
        form = TopicForm()
    else:
        #Dados do método POST enviados, processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('success'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def success(request):
    """Página de confirmação de envio"""
    topic = Topic.objects.last()

    #Garante que o 'success' seja visível apenas para o dono
    if topic.owner != request.user:
        raise Http404

    context = {'topic': topic}
    return render(request, 'learning_logs/success.html', context)

@login_required
def new_entry(request, topic_id):
    """Adicioa uma nova anotação ao Tópico atual"""
    topic = Topic.objects.get(id=topic_id)

    #Garante que a nova anotação seja visível apenas para o dono
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Nenhum dado enviado. Cria formulário em branco
        form = EntryForm()
    else:
        #dados em método POST enviados
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma anotação existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #Garante que a nova anotação seja visível apenas para o dono
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Pedido inicial. Pega os dados preenchidos previamente
        form = EntryForm(instance=entry)
    else:
        #dados do método POST serão atualizados
        form= EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def remove_entry(request, entry_id):
    """Remove uma anotação existente"""
    entry = Entry.objects.get(id=entry_id)
    topic_id = entry.topic.id
    entry.delete()
    return HttpResponseRedirect(reverse('topic', args=[topic_id]))

def erro_404(request):
    return render(request, '404.html', status=404)