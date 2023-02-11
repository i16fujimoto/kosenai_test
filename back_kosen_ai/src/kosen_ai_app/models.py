from djongo import models
from .fields import ListField
from bson.objectid import ObjectId

# Create your models here.


class Content(models.Model):
    TARGET_CHOICES = [
        ("parents", "親"),
        ("student", "学生"),
    ]

    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    content = models.CharField(max_length=50, unique=True)
    target = models.CharField(max_length=50, choices=TARGET_CHOICES)
    access_cnt = models.IntegerField(default=0)
    explanation_detail = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.content


class AccessContent(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    content_id = models.CharField(max_length=50)
    content_result = models.CharField(max_length=50)


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50, default="test", null=True, blank=True)
    kosen_name = models.CharField(max_length=50, default="test", null=True, blank=True)
    major = models.CharField(max_length=50, default="test", null=True, blank=True)
    email = models.EmailField(
        max_length=100, default="test@example.com", null=True, blank=True
    )
    password = models.CharField(max_length=50, null=True, blank=True)
    access_content = models.EmbeddedField(AccessContent)

    def __str__(self) -> str:
        return "null" if self.name is None else self.name


class type_classification_content_Weight(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    weight_study_env = models.IntegerField()
    weight_mind = models.IntegerField()
    weight_process = models.IntegerField()


class Question(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, to_field="content")
    question = models.CharField(max_length=50)
    options = ListField(val_type=str, max_length=50)
    weight = models.ArrayField(type_classification_content_Weight)
    img = models.CharField(max_length=50)
    correct_answer = models.CharField(max_length=50, null=True, blank=True)
    explanation_number = models.IntegerField(null=True, blank=True)
    explanation_title = models.CharField(max_length=50, null=True, blank=True)
    explanation_image = models.CharField(max_length=100)
    explanation_detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question


class Param(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    study_env = models.IntegerField()
    mind = models.IntegerField()
    process = models.IntegerField()


class type_classification_content_Type(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    type = models.CharField(max_length=50)
    type_img = models.CharField(max_length=100)
    type_title = models.CharField(max_length=50)
    type_advice = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.type


class type_classification_content_Result(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(type_classification_content_Type, on_delete=models.CASCADE)
    params = models.EmbeddedField(Param)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChosenAnswer(models.Model):
    _id = models.ObjectIdField()
    question_id = models.CharField(max_length=50)
    select_option = models.CharField(max_length=100)


class Answer(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    chosen_answer = models.ArrayField(ChosenAnswer)
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.content.content}_{self.user.name}"
