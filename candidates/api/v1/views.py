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

    def get(self, request):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response(
                {"error": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_words = query.split()

        queryset = self.get_queryset()

        # Annotate the queryset with a relevance based on the number of matching terms
        for i, term in enumerate(search_words, start=1):
            queryset = queryset.annotate(
                **{
                    f"match_{i}": Case(
                        When(name__icontains=term, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                }
            )

        # Sum up the matches to get the final relevance
        queryset = queryset.annotate(
            relevance=sum(
                Case(
                    When(**{f"match_{i}": 1}, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                for i in range(1, len(search_words) + 1)
            )
        )

        # Filter out candidates with a relevance greater than 0 (optional)
        queryset = queryset.filter(relevance__gt=0)

        # Order by relevance in descending order (optional)
        queryset = queryset.order_by("-relevance")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CandidateSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serialize the queryset
        serializer = CandidateSerializer(queryset, many=True)
        return Response(serializer.data)
