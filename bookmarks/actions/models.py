from django.db import models
from django.contrib.auth.models import User
#ContentType is useful for accesing the models across different applications
from django.contrib.contenttypes.models import ContentType
#Useful for building the relationship between two fields
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
      user = models.ForeignKey(User,
                            related_name='actions',
                            db_index=True)
      verb = models.CharField(max_length=255)

      #Below code is for setting up the contenttypes
      #This is used for identifying the model , ContentType instnace of a model
      target_ct = models.ForeignKey(ContentType,
                                    blank=True,
                                    null=True,
                                    related_name='target_obj')

     #to get the primary key of related object
      target_id = models.PositiveIntegerField(null=True,
                                             blank=True,
                                             db_index=True)
     #To build the relationship between model var and object primary key
      target = GenericForeignKey('target_ct', 'target_id')

      created = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
      class Meta:
          ordering = ('-created',)
