from django.db.models import Case, IntegerField, Value, When
from rest_framework import generics, status
from rest_framework.response import Response

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        queryset = Candidate.objects.all().order_by("-id")
        return queryset


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateSearchAPIView(generics.GenericAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get(self, request):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response(
                {"error": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_words = query.split()

        # Create a list of conditions for matching terms
        conditions = [
            When(name__icontains=term, then=Value(1)) for term in search_words
        ]

        # Annotate the queryset with the sum of matches
        queryset = self.get_queryset().annotate(
            relevance=sum(
                Case(
                    condition,
                    default=Value(0),
                    output_field=IntegerField(),
                )
                for condition in conditions
            )
        )
        print(queryset)

        # Filter and order by relevance
        queryset = queryset.filter(relevance__gt=0).order_by("-relevance")

        # Paginate and serialize the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
