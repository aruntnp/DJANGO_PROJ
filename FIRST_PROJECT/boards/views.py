from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .models import Board, Topic, Post


# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {'boards': boards}

    return render(request, 'home.html', context)


def board_topics(request, pk):
    b_topics = get_object_or_404(Board, pk=pk)
    context = {'boards': b_topics}

    return render(request, 'topic.html', context)


def new_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
