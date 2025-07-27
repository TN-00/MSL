from django.contrib import admin
# Registering  models here.
from .models import Label, Signimg

admin.site.register(Label)
admin.site.register(Signimg)


class SignimgAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_at', 'label')

#     search_fields = ('title', 'description')
#     list_filter = ('uploaded_at', 'label')
#     ordering = ('-uploaded_at',)
#     fields = ('title', 'description', 'signimg_img', 'video', 'label')
#     readonly_fields = ('uploaded_at',)
#     list_per_page = 20
#     save_on_top = True
    actions = None  # Disable actions for the Signimg model

 