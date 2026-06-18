from django.contrib import admin
from .models import Event, Announcement, Registration, SiteSettings
from .models import Event, Announcement, Registration, SiteSettings, HackathonTeam, TeamMember

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'event_type', 'date', 'time', 'venue', 'is_active']
    list_filter   = ['event_type', 'is_active']
    search_fields = ['title', 'venue']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ['title', 'category', 'is_published', 'publish_date', 'created_at']
    list_filter   = ['category', 'is_published']
    search_fields = ['title', 'content']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'email', 'event', 'registered_at']
    list_filter   = ['event']
    readonly_fields = ['registered_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()




class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(HackathonTeam)
class HackathonTeamAdmin(admin.ModelAdmin):
    list_display  = ['team_name', 'team_leader_name', 'event', 'registered_at']
    list_filter   = ['event']
    search_fields = ['team_name', 'team_leader_name', 'team_leader_email']
    inlines       = [TeamMemberInline]

from .models import Speaker, Sponsor, ProgramSchedule

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display  = ['name', 'position', 'event', 'order']
    list_filter   = ['event']
    search_fields = ['name', 'position']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display  = ['name', 'tier', 'event', 'order']
    list_filter   = ['event', 'tier']
    search_fields = ['name']


@admin.register(ProgramSchedule)
class ProgramScheduleAdmin(admin.ModelAdmin):
    list_display  = ['activity', 'time', 'event', 'order']
    list_filter   = ['event']