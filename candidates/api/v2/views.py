from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from rest_framework import filters, generics
from rest_framework.response import Response

from candidates.api.v1.serializers import CandidateSerializer
from candidates.models import Candidate

from .services import CandidateService


class CandidateListCreateView(generics.GenericAPIView):
    serializer_class = CandidateSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = CandidateService().get_candidates()
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            CandidateService().create_candidate(serializer.validated_data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CandidateAPIView(generics.GenericAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return CandidateService().get_candidates()

    def get(self, request, pk):
        candidate = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class(candidate)
        return Response(serializer.data)

    def put(self, request, pk):
        candidate = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class(candidate, data=request.data)
        if serializer.is_valid():
            CandidateService().update_candidate(candidate, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        candidate = self.get_queryset().get(pk=pk)
        serializer = self.serializer_class(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            CandidateService().update_candidate(candidate, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        candidate = self.get_queryset().get(pk=pk)
        candidate.delete()
        return Response(status=204)


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

        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
