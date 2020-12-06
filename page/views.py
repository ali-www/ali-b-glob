from django.shortcuts import render,get_object_or_404,redirect
from django.http import  HttpResponse, request
from .models import Board
from .models import Topic,Post
from .forms import NewTopicForm , PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request,'page/home.html',{'boards':boards})
#================================================================= star details================    
    
    
def board_topics(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    topics = board.topics.order_by('-created_dt').annotate(comments=Count('posts'))#= to know how many comments ===
    return render(request,'page/topics.html',{'board':board,'topics':topics})
#==================================================================== end details =============    

#====================================================================== start for new post form  ======================
@login_required()    
def new_topic(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    form = NewTopicForm()
    #user = User.objects.first()
    if request.method == "POST":
        form =NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by = request.user,
                topic=topic

            )
            return redirect('board_topics',board_id=board.pk)
    else:
        form = NewTopicForm()
   

    return render(request,'page/new_topic.html',{'board':board,'form':form}) 
#================================================================================ end  for new post form  ======================


#===================================================================== start details of  topic ===========================
def topic_posts(request,board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    topic.views +=1 #======= count the views =========
    topic.save()
    return render(request,'page/topic_posts.html',{'topic':topic})
#===================================================================     end details of topic ================

#======================================================================== star replay form ===========
@login_required
def reply_topic(request, board_id,topic_id):
    topic = get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    if request.method == "POST":
        form =PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            return redirect('topic_posts',board_id=board_id, topic_id = topic_id)
    else:
        form = PostForm()
    return render(request,'page/reply_topic.html',{'topic':topic,'form':form})    
#================================================================================== end  replay form ===========    