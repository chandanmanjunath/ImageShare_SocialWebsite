from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
class ImageCreateForm(forms.ModelForm):
    class Meta:
        #To use the model image
        model = Image
        #To use 3 fields from the model
        fields = ('title', 'url', 'description')
        #to make the url to be <hidden> from HTML
        widgets = {
                    'url': forms.HiddenInput,
                    }
    #By default this method is executed when is_valid is invoked
    #Syntax: clean_field_name (here field_name refered to URL)
    def clean_url(self):
        #Get the value for key URL from form
        url = self.cleaned_data['url']
        #Check the valid extensions for jpg or jpeg
        valid_extensions = ['jpg', 'jpeg']
        #Get the extension value through rsplit and convert into lower of that
        extension = url.rsplit('.', 1)[1].lower()
        #Check if its not in valid_extensions to raise a exception
        if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not ' \
                                            'match valid image extensions.')
        #return the URL
        return url

    def save(self, force_insert=False,
            force_update=False,
            commit=True):
        #to access the save of the base class
        image = super(ImageCreateForm, self).save(commit=False)
        #get the image url
        image_url = self.cleaned_data['url']
        #Formulate the image name
        image_name = '{}.{}'.format(slugify(image.title),
                                            image_url.rsplit('.', 1)[1].lower())
        # download image from the given URL
        response = request.urlopen(image_url)
        #Save the image (acess models image,then image object  of save method )
        #get all details using ContentFile
        image.image.save(image_name,
                        ContentFile(response.read()),
                        save=False)
        #if commit is true use models save
        if commit:
            image.save()
        #return the image
        return image
