from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Proposal
from .serializers import ProposalRespondSerializer, ProposalSerializer


@api_view(['GET'])
def health(_request):
    return Response({'status': 'ok'})


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all().order_by('-created_at')
    serializer_class = ProposalSerializer

    @action(detail=True, methods=['post'], url_path='respond')
    def respond(self, request, *args, **kwargs):
        proposal: Proposal = self.get_object()

        serializer = ProposalRespondSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            proposal.respond(serializer.validated_data['response'])
        except ValueError as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(ProposalSerializer(proposal).data)
