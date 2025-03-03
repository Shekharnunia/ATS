from django.db import models
from django.db.models import Q
from rest_framework import filters, generics

from candidates.api.v1.serializers import CandidateSerializer
from candidates.models import Candidate


class CandidateListCreateView(generics.ListCreateAPIView):
    serializer_class = CandidateSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = Candidate.objects.all().order_by("-id")
        return queryset


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateSearchView(generics.ListAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get("q", "")
        search_terms = search_query.split()

        # Build a Q object for each term in the search query
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(name__icontains=term)

        # Annotate candidates with the number of matching terms
        queryset = (
            Candidate.objects.filter(q_objects)
            .annotate(
                relevancy=models.Count(
                    *[
                        models.Case(
                            models.When(name__icontains=term, then=1),
                            output_field=models.IntegerField(),
                        )
                        for term in search_terms
                    ]
                )
            )
            .order_by("-relevancy")
        )

        return queryset
