from rest_framework import permissions
from rest_framework import viewsets

from surveys.models import Survey, Section, QuestionType, OptionGroup, OptionChoice, Question
from surveys.serializers import SurveySerializer, SectionSerializer, QuestionTypeSerializer, OptionGroupSerializer, \
    OptionChoiceSerializer, QuestionSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionTypeViewSet(viewsets.ModelViewSet):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class OptionGroupViewSet(viewsets.ModelViewSet):
    queryset = OptionGroup.objects.all()
    serializer_class = OptionGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class OptionChoiceViewSet(viewsets.ModelViewSet):
    queryset = OptionChoice.objects.all()
    serializer_class = OptionChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
