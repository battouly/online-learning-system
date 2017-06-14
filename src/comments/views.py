
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404

# Create your views here.

from notifications.signals import notify

from videos.models import Video

from .models import Comment, CommentBlog
from .forms import CommentForm,CommentBlogForm


@login_required
def comment_thread(request, id):
	comment = get_object_or_404(Comment, id=id)
	form = CommentForm()
	context = {
	"form": form,
	"comment": comment,
	}
	return render(request, "comments/comment_thread.html", context)



def comment_create_view(request):
	if request.method == "POST" and request.user.is_authenticated():
		parent_id = request.POST.get('parent_id')
		video_id = request.POST.get("video_id")
		origin_path = request.POST.get("origin_path")
		try:
			video = Video.objects.get(id=video_id)
		except:
			video = None

		print video
		parent_comment = None
		if parent_id is not None:
			try:
				parent_comment = Comment.objects.get(id=parent_id)
			except:
				parent_comment = None

			if parent_comment is not None and parent_comment.video is not None:
				video = parent_comment.video

		form = CommentForm(request.POST)
		if form.is_valid():
			comment_text = form.cleaned_data['comment']
			if parent_comment is not None:
				# parent comments exists
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=parent_comment.get_origin, 
					text=comment_text,
					video = video,
					parent=parent_comment
					)
				affected_users = parent_comment.get_affected_users()
				notify.send(
						request.user, 
						action=new_comment, 
						target=parent_comment, 
						recipient=parent_comment.user,
						affected_users = affected_users,
						verb='replied to')
				messages.success(request, "Thank you for your response.", extra_tags='safe')
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			else:
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=origin_path, 
					text=comment_text,
					video = video
					)
				# option to send to super user or staff users
				notify.send(
						request.user, 
						recipient = request.user, 
						action=new_comment, 
						target = new_comment.video,
						verb='commented on')
				#notify.send(request.user, recipient=request.user, action='New comment added')
				messages.success(request, "Thank you for the comment.")
				return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			print origin_path
			messages.error(request, "There was an error with your comment.")
			return HttpResponseRedirect(origin_path)

	else:
		raise Http404


@login_required #(login_url='/login/') #LOGIN_URL = '/login/'
def comment_delete_Blog(request, id):
    try:
        obj = CommentBlog.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        #messages.success(request, "You do not have permission to view this.")
        #raise Http404
        reponse = HttpResponse("You do not have permission to do this.")
        reponse.status_code = 403
        return reponse
        #return render(request, "confirm_delete.html", context, status_code=403)

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj
    }
    return render(request, "posts/confirm_delete.html", context)

def comment_thread_Blog(request, id):
    #obj = Comment.objects.get(id=id)
    try:
        obj = CommentBlog.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent

    content_object = obj.content_object # Post that the comment is on
    content_id = obj.content_object.id

    initial_data = {
            "content_type": obj.content_type,
            "object_id": obj.object_id
    }
    form = CommentBlogForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = CommentBlog.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_comment, created = CommentBlog.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


    context = {
        "comment": obj,
        "form": form,
    }
    return render(request, "posts/comment_thread.html", context)