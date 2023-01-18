from forums.models import Post



# Search function
def searchFunction(request):
    posts = Post.objects.all()  # get all the post objects
    context = {}  # initialize context dictionary

    if "search" in request.GET:  # check the request for the "search" name
        query = request.GET.get("q")  # get the search query from form (q named input)
        search_type = request.GET.get("search-type")  # get variable from dropdown box selection (search-type)

        # filter search results
        if search_type == "descriptions":  # search by description
            results = posts.filter(content__icontains=query)
        else:  # search by titles
            results = posts.filter(title__icontains=query)

        context.update({
            "results":results,
            "query":query,
        })  # update the context dictionary


    return context