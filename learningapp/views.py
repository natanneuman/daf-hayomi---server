from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from learningapp.models import StudyPlan, DafLearned
from learningapp.serializers import StudyPlanSerializer, DafSerializer, CurrentUserSerializer, \
    UserSerializer


# class StudyPlanApiView(APIView):
#
#     def get(self, request):
#         data = StudyPlan.objects.all()
#         serializer = StudyPlanSerializer(data=data, many=True)
#         if serializer.is_valid():
#             return Response(serializer.data)
#         return Response(serializer.errors)


# class ListCreateStudyPlanView(generics.ListCreateAPIView):
#     queryset = StudyPlan.objects.all()
#     serializer_class = StudyPlanSerializer
#
#
# class DetailStudyPlanView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = StudyPlan.objects.all()
#     serializer_class = StudyPlanSerializer


class StudyPlanViewSet(ModelViewSet):
    serializer_class = StudyPlanSerializer
    def get_queryset(self):
        active = self.request.query_params.get("active")
        if active:
            return StudyPlan.objects.filter(active=True)
        return StudyPlan.objects.all()


class DafLearnedView(generics.CreateAPIView):
    queryset = DafLearned.objects.all()
    serializer_class = DafSerializer


class DafLearnedDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DafLearned.objects.all()
    serializer_class = DafSerializer


class StudyPlanBackup(generics.GenericAPIView):
    serializer = DafSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        for plan in request.data:
            plan_id = plan.get("id")
            study_plan = StudyPlan.objects.filter(id=plan_id)[0]
            study_plan.dafim.all().delete()
            for daf in plan['dafLearned']:
                serializer = self.serializer(data=daf)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer


class RegisterUser(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["token"] = str(token)
        return response

class CustomAuthToken(ObtainAuthToken):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })