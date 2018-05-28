from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone

#generic function to create the action
def create_action(user, verb, target=None):
        # check for any similar action made in the last minute
        #get the current the current time
        now = timezone.now()
        #get the last minute time
        last_minute = now - datetime.timedelta(seconds=60)
        #get all the actions performed by user in last minute
        #timestamp__gte is the start timei.e. from (for end time use timestamp__lte )
        similar_actions = Action.objects.filter(user_id=user.id,
                                                verb= verb,
                                                created__gte=last_minute)
        #get the target object
        if target:
            #if target exists then get the content type instance by passing the target object
            target_ct = ContentType.objects.get_for_model(target)
            #filter the targeted object from similar_actions to get current action is performed previously or not
            similar_actions = similar_actions.filter(target_ct=target_ct,
                                                    target_id=target.id)
        #if no similar_actions
        if not similar_actions:
            # no existing actions found
            #create a new action
            action = Action(user=user, verb=verb, target=target)
            #save the action since its not performed previously
            action.save()
            return True
        return False
