from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    Content,
    User,
    Answer,
    ChosenAnswer,
    Question,
    type_classification_content_Result,
)
from .s3 import fetch_file_from_s3


class ContentSerializer(ModelSerializer):
    content_id = SerializerMethodField()

    class Meta:
        model = Content
        fields = ("content_id", "content")

    def get_content_id(self, instance):
        return str(instance._id)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "_id",
            "name",
            "kosen_name",
            "major",
            "email",
            "password",
        )
        read_only_fields = ("_id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }


class DiagnosisSerializer(ModelSerializer):
    question_id = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = Question
        fields = ("question", "question_id", "options", "image")

    def get_question_id(self, instance):
        return str(instance._id)

    def get_image(self, instance):
        return fetch_file_from_s3(instance.img)


class ResultSerializer(ModelSerializer):
    result_title = SerializerMethodField()
    result_type = SerializerMethodField()
    result_type_img = SerializerMethodField()
    result_advice = SerializerMethodField()
    result_param = SerializerMethodField()

    class Meta:
        model = type_classification_content_Result
        fields = (
            "result_title",
            "result_type",
            "result_type_img",
            "result_advice",
            "result_param",
        )

    def get_result_title(self, instance):
        return instance.type.type_title

    def get_result_type(self, instance):
        return instance.type.type

    def get_result_type_img(self, instance):
        return fetch_file_from_s3(instance.type.type_img)

    def get_result_advice(self, instance):
        return instance.type.type_advice

    def get_result_param(self, instance):
        params = instance.params
        params.pop("_id")
        return params
