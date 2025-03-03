import django_filters
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

from candidates.models import Candidate


class CandidateFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")

    def filter_q(self, queryset, name, value):
        query_words = value.strip().split()
        filters = Q()
        for word in query_words:
            filters |= Q(name__icontains=word)

        return (
            queryset.filter(filters)
            .annotate(relevance=TrigramSimilarity("name", value))
            .order_by("-relevance")
        )

    class Meta:
        model = Candidate
        fields = ["q"]
