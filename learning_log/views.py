from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from learning_log.forms import EntryForm, TopicForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """The Home for Learning Log"""
    return render(request, 'index.html')

@login_required
def topics(request):
    """show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request,'topics.html',context)

@login_required
def topic(request, topic_id):
    """show a single topic and all its entries"""
    topics = Topic.objects.get(id=topic_id)
    entries = topics.entry_set.order_by('-date_added')
    context = {'topic': topics, 'entries': entries}
    return render(request,'topic.html',context)

@login_required
def new_topic(request):
    """Add a new Topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.owner = request.user
            return HttpResponseRedirect(reverse('learning_log:topics'))

    context = {'form': form}
    return render(request,'new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for particular Topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_log:topic', args=[topic_id]))

    context = {'topic':topic, 'form': form}
    return render(request,'new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry for particular Topic"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_log:topic', args=[topic.id]))

    context = {'entry':entry, 'topic': topic, 'form': form}
    return render(request,'edit_entry.html', context)