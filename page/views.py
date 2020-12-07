from django.core import paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.http import  HttpResponse, request
from .models import Board
from .models import Topic,Post
from .forms import NewTopicForm , PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, query
from django.views.generic import UpdateView ,ListView
from django.utils import timezone
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.




class BoardListView(ListView):
    model = Board 
    template_name = 'page/home.html'
    context_object_name = 'boards'
#================================================================= star details================    
    
    
def board_topics(request,board_id):
    board = get_object_or_404(Board,pk=board_id)
    queryset = board.topics.order_by('-created_dt').annotate(comments=Count('posts'))
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,2)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)     
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
    
    session_key = 'view_topic_{}'.format(topic.pk) #======= start count the views =========
    if not request.session.get(session_key,False):
        topic.views +=1
        topic.save()
        request.session[session_key] = True  #=======  end count the views =========
    
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

@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'page/edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts',board_id=post.topic.board.pk,topic_id=post.topic.pk)