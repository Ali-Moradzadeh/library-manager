from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from managing.models import Book, Popularity


class SetCommentsAndRepliesLikeDisLike(View) :
    ACTIONS = {
        "LIKE" : "+",
        "DISLIKE" : "-"
    }
    
    def dispatch(self, request, *args, **kwargs) :
        if "next" not in kwargs :
            kwargs["next"] = addresses.land_url
        
        action = kwargs["action"].upper()
        self.user_requested_action = self.ACTIONS[action]
        
        self.app_label = kwargs["class"].split("_")[0]
        self.model_name = "_".join(kwargs["class"].split("_")[1:])
        self.content_type = ContentType.objects.get(app_label=self.app_label, model=self.model_name)
        
        related_model_obj = self.content_type.model_class().objects.get(id=kwargs["id"])
        
        if related_model_obj.user == request.user :
            return redirect(kwargs["next"])
        
        self.popularity = Popularity.objects.filter(user=request.user, content_type=self.content_type, object_id=kwargs["id"])
        
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs) :
        
        if self.popularity.exists() :
            self.popularity = self.popularity[0]
            
            if self.popularity.action != (act := self.user_requested_action) :
                previous = self.popularity.get_action_display()
                
                self.popularity.action = act
                self.popularity.save()
                act.capitalize()
                messages.success(request, f"your {previous} was successfully changes to {self.popularity.get_action_display()}", "alert")
            else :
                self.popularity.delete()
                messages.success(request, f"your {self.popularity.get_action_display()} was successfully removed", "alert")
        else :
            popularity = Popularity(user=request.user, content_type=self.content_type, object_id=kwargs["id"], action=self.user_requested_action)
            popularity.save()
            messages.success(request, f"your {popularity.get_action_display()} was successfully saved", "alert")

        return redirect(kwargs["next"])

