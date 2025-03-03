from django.utils import timezone
from rest_framework import serializers

from candidates.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    date_of_birth = serializers.DateField(format="%d-%m-%Y", write_only=True)

    def get_age(self, obj: Candidate) -> int:
        # calculate age from date_of_birth
        return (timezone.now().date() - obj.date_of_birth).days // 365

    class Meta:
        model = Candidate
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "email",
            "phone_number",
            "date_of_birth",
        ]
