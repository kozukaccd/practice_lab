from django.contrib import admin
from .models import Question, Choice


# Register your models here.

class ChoiceInline(admin.TabularInline):  # tutorial07
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ["pub_date", "question_text"] # adminサイトでのフィールドの並び順
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Data information.", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]  # adminサイトでのフォームをフィールドセットで分割
    inlines = [ChoiceInline]

    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
