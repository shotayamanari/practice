# redirectを追加
from django.shortcuts import render,redirect
# LoginRequiredMixinを追加
from django.contrib.auth.mixins import LoginRequiredMixin
# Viewを追加
from django.views import View

# modelsの追加
from .models import Topic,Tag
# formの追加
from .forms import TopicForm,TopicTagForm

# Queryの追加
from django.db.models import Q


class IndexView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        context = {}
        context["tags"]     = Tag.objects.all()

        query   = Q()

        if "search" in request.GET:
            search      = request.GET["search"]

            raw_words   = search.replace("　"," ").split(" ")
            words       = [ w for w in raw_words if w != "" ]

            for w in words:
                query &= Q(title__contains=w)
        
        # queryによる検索
        topics  = Topic.objects.filter(query).order_by("-dt")

        # タグの検索(指定されたタグが実在するのか確認する)
        form    = TopicTagForm(request.GET)

        if form.is_valid():
            cleaned         = form.clean()
            selected_tags   = cleaned["tag"]

            # タグ検索をする
            for tag in selected_tags:

                topics      = [ topic for topic in topics if tag in topic.tag.all() ]
            
        context["topics"]   = topics

        return render(request,"search/index.html",context)
    
    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = TopicForm(copied)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("search:index")
        
        print("バリデーションOK")
        form.save()

        return redirect("search:index")

index = IndexView.as_view()


class AddTagView(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        
        topic   = Topic.objects.filter(id=pk).first()
        form    = TopicTagForm(request.POST)

        if form.is_valid():
            cleaned         = form.clean()
            selected_tags   = cleaned["tag"]

            for tag in selected_tags:
                if tag in topic.tag.all():
                    topic.tag.remove(tag)
                else:
                    topic.tag.add(tag)

        return redirect("search:index")

tag = AddTagView.as_view()