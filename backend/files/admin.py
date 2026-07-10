from django.contrib import admin
from .models import UploadSession, UploadSessionFile, File

admin.site.register(UploadSession)
admin.site.register(UploadSessionFile)
admin.site.register(File)
