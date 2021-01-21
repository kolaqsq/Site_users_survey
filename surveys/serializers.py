from rest_framework import serializers

from surveys.models import Survey, Section


class SurveySerializer(serializers.ModelSerializer):
    # section = SectionSerializer()

    class Meta:
        model = Survey
        fields = '__all__'
        # depth = 3


class SectionSerializer(serializers.ModelSerializer):
    survey = SurveySerializer()

    class Meta:
        model = Section
        fields = [
            'id',
            'creator',
            'survey',
            'section_title',
            'section_desc',
        ]
