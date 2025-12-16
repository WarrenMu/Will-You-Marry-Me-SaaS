from django.contrib import admin

from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposer_name', 'proposee_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'proposer_name', 'proposee_name', 'message')
