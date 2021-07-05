from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class DafSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = DafLearned
        fields = ('id', 'study_plan', 'masechet_name', 'page_number', 'chazara', 'index_in_list_dafs', 'created_on')
        # depth = 1


class StudyPlanSerializer(serializers.ModelSerializer):
    dafLearned = DafSerializer(read_only=True, many=True, source='daflearned_set')
    class Meta:
        model = StudyPlan
        fields = ('id', 'user', 'typeOfStudy', 'wantChazara', 'dafLearned', 'active')
        # fields = '__all__'


class CurrentUserSerializer(serializers.ModelSerializer):
    study_plans = StudyPlanSerializer(read_only=True, many=True, source='studyplan_set')
    class Meta:
        model = User
        fields = ('username', 'id', 'study_plans')





class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ( "id", "username", "password", )