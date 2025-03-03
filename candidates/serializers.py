from datetime import date

from django.utils import timezone
from rest_framework import serializers

from candidates.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    date_of_birth = serializers.DateField(format="%d-%m-%Y", write_only=True)

    def get_age(self, obj: Candidate) -> int:
        # calculate age from date_of_birth
        return (timezone.now().date() - obj.date_of_birth).days // 365

    def validate_date_of_birth(self, value: date) -> date:
        # validate date_of_birth
        print(value)
        print(type(value))
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

    def validate_phone_number(self, value: str) -> str:
        # validate phone_number
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits")
        return value

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
