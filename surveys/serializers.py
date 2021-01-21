from rest_framework import serializers

from surveys.models import Survey, Section, QuestionType, OptionGroup, OptionChoice, Question


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()

    class Meta:
        model = Section
        fields = '__all__'


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'


class OptionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionGroup
        fields = '__all__'


class OptionChoiceSerializer(serializers.ModelSerializer):
    group = OptionGroupSerializer()

    class Meta:
        model = OptionChoice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    question_type = QuestionTypeSerializer()
    option_group = OptionGroupSerializer()

    class Meta:
        model = Question
        fields = '__all__'
