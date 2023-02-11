from django.contrib import admin
from .models import (
    Answer,
    Content,
    User,
    Question,
    type_classification_content_Type,
    type_classification_content_Result,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Content)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(type_classification_content_Type)
admin.site.register(type_classification_content_Result)
