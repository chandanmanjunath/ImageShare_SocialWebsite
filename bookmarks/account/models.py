from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
        #Creating one to one relationship with user model
        user = models.OneToOneField(settings.AUTH_USER_MODEL)
        #null is True related to default null in db
        #blank is True related to form validation,field can be left blank in form
        date_of_birth = models.DateField(blank=True, null=True)
        #defining the image field
        photo = models.ImageField(upload_to='users/%Y/%m/%d',
                                  blank=True)
        #The below method is for human readable representaion of an object
        #Here we are represtig user object
        def __str__(self):
                return 'Profile for user {}'.format(self.user.username)

#This model is used to implement follower/followed by feature not directly using many to many relationship
class Contact(models.Model):
        #The user who follows
        user_from = models.ForeignKey(User,related_name='rel_from_set')
        #The user who is followed by
        user_to = models.ForeignKey(User,related_name='rel_to_set')
        #Time when the data got created
        created = models.DateTimeField(auto_now_add=True,db_index=True)

        #order based on created descending(- indicates descending)
        class Meta:
            ordering = ('-created',)
        #representation of an object
        def __str__(self):
            return '{} follows {}'.format(self.user_from,self.user_to)

# Add following field to User dynamically since its provided by django we dont edit it diractly
#symmetrical is when  a user might follow another user where as another user need not follow same user
User.add_to_class('following',
                 models.ManyToManyField('self',
                 through=Contact,#use the Contact class
                 related_name='followers',#name it as followers
                 symmetrical=False))#symmetrical is false since its true by default
