from rest_framework import serializers

from intranet.academic.models import Curriculum, ManagementUnit, CurriculumCourse


class ManagementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementUnit
        exclude = ['is_trash' , 'lft', 'rght', 'tree_id', 'trashed_by', 'trashed_at']

    parent = serializers.SlugRelatedField(
        slug_field='code',
        queryset=ManagementUnit.objects.all()
    )


class CurriculumCourseInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumCourse
        exclude = [
            'curriculum',
            'is_trash', 
            'trashed_at', 
            'reg_number', 
            'inner_id', 
            'trashed_by'
            ]

    course = serializers.StringRelatedField()
    concentration = serializers.StringRelatedField(many=True)


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

    rmu = ManagementUnitSerializer()
    curriculum_courses = CurriculumCourseInlineSerializer(many=True, required=False)