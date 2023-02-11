from typing import Dict

from bson.objectid import ObjectId
from rest_framework import views
from rest_framework.response import Response

from .models import (Answer, Content, Question, User,
                     type_classification_content_Result,
                     type_classification_content_Type)
from .serializers import (ContentSerializer, DiagnosisSerializer,
                          ResultSerializer, UserSerializer)

# Create your views here.


class GetContents(views.APIView):
    def get(self, request):
        user = UserSerializer(
            data={
                "name": None,
                "kosen_name": None,
                "major": None,
                "email": None,
                "password": None,
            }
        )
        if user.is_valid():
            user.save()

        contents = Content.objects.all()
        content_data = ContentSerializer(contents, many=True).data

        return Response(
            {"user_id": user.data["_id"], "contents": content_data}, status=200
        )


class GetDiagnosis(views.APIView):
    def get(self, request):
        content_id: ObjectId = ObjectId(request.GET.get("content_id"))

        try:
            content = Content.objects.get(_id=content_id)
            content.access_cnt += 1
            content.save()
            content = content.content
        except Content.DoesNotExist:
            content = None

        questions = Question.objects.filter(content___id=content_id)
        question_data = DiagnosisSerializer(questions, many=True).data

        return Response({"content": content, "questions": question_data}, status=200)


class GetResult(views.APIView):
    def post(self, request):
        user_id: str = request.data.get("user_id")
        content_id: str = request.data.get("content_id")

        user = User.objects.get(_id=ObjectId(user_id))
        content = Content.objects.get(_id=ObjectId(content_id))

        for answer_dict in request.data.get("answer_list"):
            answer_dict["_id"] = ObjectId()

            answer, created = Answer.objects.get_or_create(user=user, content=content)
            if created:
                answer.chosen_answer = [answer_dict]
            else:
                answer.chosen_answer.append(answer_dict)
            answer.save()

        answer = Answer.objects.get(user=user, content=content)

        result_param = self.calc_param(answer)
        result_type = self.decide_type(result_param)

        result_param["_id"] = ObjectId()
        result = type_classification_content_Result.objects.create(
            user=user,
            type=result_type,
            params=result_param,
        )
        result.save()

        user.access_content = {
            "_id": ObjectId(),
            "content_id": content_id,
            "content_result": str(result._id),
        }
        user.save()

        result_data = ResultSerializer(result).data

        return Response(result_data, status=200)

    @staticmethod
    def calc_param(answer) -> Dict[str, int]:
        result_param: Dict[str, int] = {
            "study_env": 0,
            "mind": 0,
            "process": 0,
        }

        for chosen_answer in answer.chosen_answer:
            question_id: str = chosen_answer["question_id"]
            select_option: str = chosen_answer["select_option"]

            question = Question.objects.get(_id=ObjectId(question_id))
            choice: int = question.options.index(select_option)

            weights: Dict[str, int] = question.weight[choice]
            for param_name in ["study_env", "mind", "process"]:
                result_param[param_name] += weights[f"weight_{param_name}"]

        return result_param

    @staticmethod
    def decide_type(result_param):
        study_env = "S" if result_param["study_env"] < 22.5 else "P"
        mind = "D" if result_param["mind"] < 22.5 else "R"
        process = "F" if result_param["process"] < 22.5 else "L"

        return type_classification_content_Type.objects.get(
            type=f"{study_env}{mind}{process}"
        )

    # NOTE: 使わなくなったViewを一旦コメントアウト
    """
    def patch(self, request):
        user_id: str = request.data.get("user_id")
        content_id: str = request.data.get("content_id")
        answer_dict: Dict[str, str] = request.data.get("answer")

        user = User.objects.get(_id=ObjectId(user_id))
        content = Content.objects.get(_id=ObjectId(content_id))

        answer = Answer.objects.get(
            user=user,
            content=content,
            chosen_answer={"question_id": answer_dict["question_id"]},
        )

        chosen_answer: List[Dict[str, str]] = answer.chosen_answer
        index = search(
            chosen_answer, lambda x: x["question_id"] == answer_dict["question_id"]
        )
        chosen_answer[index]["answer"] = answer_dict["answer"]

        answer.save()

        return Response({"result": True}, status=200)


class FinishAnswer(views.APIView):
    def patch(self, request):
        user_id: str = request.data.get("user_id")
        content_id: str = request.data.get("content_id")
        is_finish: bool = request.data.get("is_finish")

        user = User.objects.get(_id=ObjectId(user_id))
        content = Content.objects.get(_id=ObjectId(content_id))

        answer = Answer.objects.get(user=user, content=content)
        answer.is_finish = is_finish
        answer.save()

        return Response({"result": True}, status=200)
    """
