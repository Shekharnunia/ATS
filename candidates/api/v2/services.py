from candidates.models import Candidate


class CandidateService:

    def get_candidates(self):
        return Candidate.objects.all().order_by("-id")

    def create_candidate(self, data: dict):
        # take action before creating candidate
        candidate = Candidate.objects.create(**data)
        # take action after creating candidate
        return candidate

    def update_candidate(self, candidate: Candidate, data: dict):
        for key, value in data.items():
            if key in ["id", "pk"]:
                continue
            setattr(candidate, key, value)
        # take action before saving candidate
        # only update fields that have changed
        candidate.save(update_fields=data.keys())
        # take action after saving candidate
