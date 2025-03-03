from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from rest_framework import filters, generics
from rest_framework.response import Response

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    serializer_class = CandidateSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = Candidate.objects.all().order_by("-id")
        return queryset


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateSearchView(generics.GenericAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)

        query_words = query.split()

        # Generate OR conditions for each word in the query
        filters = models.Q()
        for word in query_words:
            filters |= models.Q(name__icontains=word)

        # Annotate with relevance score based on trigram similarity
        candidates = (
            Candidate.objects.filter(filters)
            .annotate(relevance=TrigramSimilarity("name", query))
            .order_by("-relevance")
        )
        page = self.paginate_queryset(candidates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(candidates, many=True)

        return Response(serializer.data)
