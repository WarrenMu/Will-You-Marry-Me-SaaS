from rest_framework import serializers

from .models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = (
            'id',
            'proposer_name',
            'proposee_name',
            'message',
            'status',
            'created_at',
            'responded_at',
        )
        read_only_fields = ('id', 'status', 'created_at', 'responded_at')


class ProposalRespondSerializer(serializers.Serializer):
    response = serializers.ChoiceField(
        choices=(Proposal.Status.ACCEPTED, Proposal.Status.REJECTED)
    )
