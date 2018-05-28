from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
#get the create_action we have just created
from actions.utils import create_action
#import the redis db
import redis
#import the settings
from django.conf import settings


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                     port=settings.REDIS_PORT,
                     db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
                # form data is valid
                cd = form.cleaned_data
                new_item = form.save(commit=False)
                # assign current user to the item
                new_item.user = request.user
                new_item.save()
                #to record the action in the database
                create_action(request.user, 'bookmarked image', new_item)
                messages.success(request, 'Image added successfully')
                # redirect to new created item detail view
                return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request,
                 'images/image/create.html',
                 {'section': 'images',
                 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    #to increment value of key
    #Syntax:  object-type(model):id:fieldname (this is overall key)
    total_views = r.incr('image:{}:views'.format(image.id))
    #add total values to dictionary
    # increment image ranking by 1
    #Below is the sorted list
    #syntax (sorted_list_name,key,amount_of_inc_value)
    #increment image_ranking sorted list for the image with given image_id by 1
    r.zincrby('image_ranking', image.id, 1)
    return render(request,
                'images/image/detail.html',
                {'section': 'images',
                'image': image,
                'total_views': total_views})



@ajax_required
@login_required
#To verify that the form method used is POST with the below decorator
@require_POST
def image_like(request):
        #get the values from get parameters
        #iamge_id
        image_id = request.POST.get('id')
        #action
        action   = request.POST.get('action')
        #if both
        if image_id and action:
            try:
                #get image objects using get method
                image = Image.objects.get(id=image_id)
                #if action is like then
                if action == 'like':
                    #users_like is the manager provided by django,use add method
                    image.users_like.add(request.user)
                    #to create a action note that the image is liked/unliked
                    create_action(request.user, 'likes', image)
                else:
                    #use remove method
                    image.users_like.remove(request.user)
                #return JsonResponse if successful
                return JsonResponse({'status':'ok'})
            except:
                pass
        #return JsonResponse if failed
        return JsonResponse({'status':'ko'})


from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
                                            PageNotAnInteger
@login_required
def image_list(request):
        #get all the image objects
        images = Image.objects.all()
        #List 8 images for each page
        paginator = Paginator(images, 8)
        #retrieve the page object
        page = request.GET.get('page')
        try:
            #pass the page to get the images
            images = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer deliver the first page,example if only 8 images are available secon time display the page 1
            images = paginator.page(1)
        #if page is empty
        except EmptyPage:
            if request.is_ajax():
                # If the request is AJAX and the page is out of range
                # return an empty page
                return HttpResponse('')
            # If page is out of range deliver last page of results
            images = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request,
                        'images/image/list_ajax.html',
                        {'section': 'images', 'images': images})
        return render(request,
                    'images/image/list.html',
                    {'section': 'images', 'images': images})




@login_required
def image_ranking(request):
          # get image ranking dictionary
          #Syntax:r.zrange(sorted_set,start,end,desc:true/false)
          #get all the elements from a sorted set order by desc and slice top 10 elements
          #get the key value pairs
          image_ranking = r.zrange('image_ranking', 0, -1,desc=True)[:10]
          #Build a id set for most viewed
          image_ranking_ids = [int(id) for id in image_ranking]
          # get most viewed images
          most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
          #Here since most_viewed.sort is used most_viewed elements are passed as argument to lambda ,and get the index of those
          #and sort with this as a key
          most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
          return render(request,
                        'images/image/ranking.html',
                        {'section': 'imagesview',
                        'most_viewed': most_viewed})
