from rest_framework import filters, generics
from rest_framework.response import Response

from candidates.models import Candidate
from candidates.serializers import CandidateSerializer

from .filters import CandidateFilter
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
        try:
            candidate = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(candidate)
            return Response(serializer.data)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=404)

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
    filterset_class = CandidateFilter

    def get_queryset(self):
        return CandidateService().get_candidates()

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)

        candidates = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(candidates)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(candidates, many=True)
        return Response(serializer.data)
