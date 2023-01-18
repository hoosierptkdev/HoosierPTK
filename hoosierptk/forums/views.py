from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Profile, Forum, Topic, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Home view
def Home(request):
    forums = Forum.objects.all()
    topics = Topic.objects.all()

    # forum stats widget functionality
    num_posts = Post.objects.all().count()  # get the total number of posts
    num_users = User.objects.all().count()  # get the total number of users
    num_topics = topics.count()  # get the total number of categories/topics (we already have the object)
    last_post = Post.objects.latest("date")  # get the latest post object

    context = {
        "forums":forums,
        "topics":topics,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_topics":num_topics,
        "last_post":last_post,
        "title":"Forums",
    }

    return render(request, "forums/home.html", context)


# Posts view
@login_required  # make sure user is signed in / authenticated
def Posts(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    posts = Post.objects.filter(approved=True, topic=topic).order_by('-date')

    # django pagination (backend)
    paginator = Paginator(posts, 5)  # paginator object (5 posts per page)
    page = request.GET.get("page")  # get the number of the current page
    # 3 paginator "try" options
    try:
        posts = paginator.page(page)  # try the current page
    except PageNotAnInteger:  # is the page number not an integer? (page 1)
        posts = paginator.page(1)
    except EmptyPage:  # is the page empty? (end of the pagination)
        posts = paginator.page(paginator.num_pages)  # display the final paginator page

    context = {
        "posts":posts,
        "topic":topic,
        "title":topic.title,
    }

    return render(request, "forums/posts.html", context)


# Detail view
@login_required  # make sure user is signed in / authenticated
def Detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    profile = Profile.objects.get(user=request.user)  # get the profile for logged in user

    # check for comment submissions / form
    if "comment-form" in request.POST:
        # print("Comment")  # test statement to print to console
        comment = request.POST.get("comment")  # get the content of the "comment" textarea
        new_comment, created = Comment.objects.get_or_create(user=profile, content=comment)  # manually create new comment instance
        post.comments.add(new_comment.id)  # link new comment to the post
        profile.points += 50  # add 50 points for a comment
        profile.save()  # save profile
        return redirect(request.META['HTTP_REFERER'])  # POST/Redirect/GET

    # check for reply submissions / form
    if "reply-form" in request.POST:
        reply = request.POST.get("reply")  # get the content of the "reply" textarea
        comment_id = request.POST.get("comment-id")  # for which comment is this a reply (get comment ID from hidden input)
        comment_obj = Comment.objects.get(id=comment_id)  # get the comment object
        new_reply, created = Reply.objects.get_or_create(user=profile, content=reply)  # manually create new reply instance
        comment_obj.replies.add(new_reply.id)  # link new reply to the comment
        profile.points += 25  # get 25 points for a reply
        profile.save()  # save profile
        return redirect(request.META['HTTP_REFERER'])  # POST/Redirect/GET

    context = {
        "post":post,
        "title":post.title,
    }

    update_views(request, post)  # update hit count

    return render(request, "forums/detail.html", context)


# Create / New Post View
@login_required  # make sure user is signed in / authenticated
def CreatePost(request):
    context = {}
    form = PostForm(request.POST or None)  # use our PostForm to access the Model

    if request.method == "POST":  # check if request method is POST
        if form.is_valid():  # check if form is valid
            profile = Profile.objects.get(user=request.user)  # get the profile from the signed in user
            new_post = form.save(commit=False)  # create a local instance of the form (commit=False = not saved to database)
            new_post.user = profile  # manually add the author to the post (from the profile we got earlier)
            new_post.save()  # save the manually updated form
            profile.points += 100  # get 100 points for a new post
            profile.save()  # save profile
            return redirect("forums:home")  # redirect user to homepage (could use a post "draft" page)

    context.update({
        "form": form,
        "title": "Create New Post",
    })  # update context dictionary to send form to the template

    return render(request, "forums/create_post.html", context)


# Latest Posts View
@login_required  # make sure user is signed in / authenticated
def LatestPosts(request):
    posts = Post.objects.all().filter(approved=True).order_by('-date')[:10]  # get the approved post objects (10 of the latest posts)

    context = {
        "posts":posts,
        "title": "Latest Posts",
    }

    return render(request, "forums/latest_posts.html", context)


# Search Results View
@login_required  # make sure user is signed in / authenticated
def SearchResults(request):

    context = {
        "title":"Search Results",
    }

    return render(request, "forums/search.html", context)