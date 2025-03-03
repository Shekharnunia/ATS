from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from rest_framework import filters, generics
from rest_framework.response import Response

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing candidates.
    post:
    Create a new candidate.
    """

    serializer_class = CandidateSerializer

    def get_queryset(self):
        queryset = Candidate.objects.all().order_by("-id")
        return queryset


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return the candidate identified by the ID.
    put:
    Update the candidate identified by the ID.
    patch:
    Partially update the candidate identified by the ID.
    delete:
    Delete the candidate identified by the ID.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateSearchView(generics.GenericAPIView):
    """
    get:
    Search for candidates based on a query string.
    """

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
