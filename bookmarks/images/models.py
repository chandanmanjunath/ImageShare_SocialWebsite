from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse

class Image(models.Model):
        #First argument refers to base class it has refered and name it as images_created
        user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='images_created')
        title = models.CharField(max_length=200)
        #the field which is used for building URL,letters,numbers,underscore,hyphens are used
        slug = models.SlugField(max_length=200,
                                blank=True)
        url = models.URLField()
        image = models.ImageField(upload_to='images/%Y/%m/%d')
        description = models.TextField(blank=True)
        #db_index=True creates the index in the data base for this field
        created = models.DateField(auto_now_add=True,
                                    db_index=True)
        #A ManyToManyField for number of likes for images by users
        #user likes multiple images
        #Image liked by multiple users
        #Many to many can be achieved like
        #users.images_liked.all() and users.users_like.all()
        users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            related_name='images_liked',
                                            blank=True)
        #total_likes for a image calculation
        total_likes = models.PositiveIntegerField(db_index=True,default=0)
        def __str__(self):
            return self.title
        #Overiding the base save method to autogenerate save to get slug valye for title
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
                #super used here is to get access to the base class methods ex.save here
                super(Image, self).save(*args, **kwargs)
        #the below method is used for building the canonical URLs using the reverse
        def get_absolute_url(self):
                #the first argument is view name
                #second is argument list
                return reverse('images:detail', args=[self.id, self.slug])
