from django.test import TestCase
from rest_framework.test import APIRequestFactory

from ..models import Content, User, Question
from ..views import GetContents, GetDiagnosis, GetResult


class APIViewTests(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.user = User.objects.all()[0]
        self.contents = Content.objects.all()

    def test_get_contents_api(self):
        factory = APIRequestFactory()
        view = GetContents.as_view()

        pre_user_num = len(User.objects.all())

        url = "/kosenai/contents"
        request = factory.get(url)
        response = view(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data["contents"]), len(Content.objects.all()))
        self.assertEquals(len(User.objects.all()), pre_user_num + 1)

    def test_get_diagnosis_api(self):
        view = GetDiagnosis.as_view()
        factory = APIRequestFactory()

        for content in self.contents:
            pre_access_cnt = content.access_cnt
            content_id = content._id
            questions = Question.objects.filter(content=content)

            url = f"/kosenai/diagnosis/?content_id={content_id}"
            request = factory.get(url)
            response = view(request)

            self.assertEquals(response.status_code, 200)
            self.assertEquals(response.data["content"], content.content)
            self.assertEquals(len(response.data["questions"]), len(questions))
            self.assertEquals(
                Content.objects.get(_id=content_id).access_cnt,
                pre_access_cnt + 1,
            )

    def test_get_result_api(self):
        factory = APIRequestFactory()
        view = GetResult.as_view()
        url = "/kosenai/result"

        for content in self.contents:
            questions = Question.objects.filter(content=content)
            payload = {
                "user_id": str(self.user._id),
                "content_id": str(content._id),
                "answer_list": [
                    {
                        "question_id": str(question._id),
                        "select_option": question.options[0],
                    }
                    for question in questions
                ],
            }
            request = factory.post(url, payload, format="json")
            response = view(request)

            self.assertEquals(response.status_code, 200)
            self.assertEquals(
                response.data.keys(),
                {
                    "result_title",
                    "result_type",
                    "result_type_img",
                    "result_advice",
                    "result_param",
                },
            )
            self.assertEquals(
                response.data["result_param"].keys(),
                {
                    "study_env",
                    "mind",
                    "process",
                },
            )
