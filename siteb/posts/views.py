from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.contrib import messages
from urllib.parse import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def post_home(request):
	return HttpResponse("<h1>hello my blog is here</h1>")

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	#if not request.user.is_authenticated():
		#raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form":form,
	}	
	return render(request,"post_form.html", context)

def post_detail(request, pk=None):
	instance = get_object_or_404(Post, id=pk)
	share_string = quote_plus(instance.content)
	context={
		"title":"Post Detail",
		"instance" : instance,
		"share_string" : share_string
	}
	return render(request,"post_detail.html", context)

def post_list(request): 
	queryset_list = Post.objects.all()#.order_by("-timestamp")
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query)).distinct()
	#here a new this pagination applied to list view
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"title":"List",
		"object_list":queryset
	}
	return render(request,"post_list.html", context)
	#return HttpResponse("<h1>list</h1>")
def post_update(request, pk=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=pk)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a>Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context={
		"title":instance.title,
		"instance" : instance,
		"form":form,
	}
	return render(request,"post_form.html", context)

	


def post_delete(request,pk=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=pk)
	instance.delete()
	messages.success(request, "successfully deleted")
	return redirect("posts:list")
