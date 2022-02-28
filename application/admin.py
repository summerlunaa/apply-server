from django.contrib import admin
from .models import Application


class DisplayApplication(admin.ModelAdmin):
   
    ordering = ('updated_at',)
    # 여기 추가
    readonly_fields = ['answer1', 'answer2','answer3','answer4','answer5']

    def has_delete_permission(self, request, obj=None):
            #Disable delete
            return False
        
    def has_add_permission(self, request, obj=None):
            #Disable add
            return False
            
    def has_change_permission(self, request, obj=None):
            #Disable update
        return False
admin.site.register(Application, DisplayApplication)