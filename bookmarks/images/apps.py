#this is used for signal registration and configurations
#the below code is used for initialization and signal import to the application
from django.apps import AppConfig
class ImagesConfig(AppConfig):
      #app name specification images(python path to application)
      name = 'images'
      #human readable name
      verbose_name = 'Image bookmarks'
      #method where we import signals
      def ready(self):
            # import signal handlers
            import images.signals
