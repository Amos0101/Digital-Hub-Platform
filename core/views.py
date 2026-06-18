from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

from .models import Event, Announcement, Registration, SiteSettings
from .forms import RegistrationForm, EventForm, AnnouncementForm

from .models import Event, Announcement, Registration, SiteSettings, HackathonTeam, TeamMember
from .forms import RegistrationForm, HackathonTeamForm, EventForm, AnnouncementForm
from .models import Speaker, Sponsor, ProgramSchedule
from .forms import SpeakerForm, SponsorForm, ProgramScheduleForm

from datetime import datetime
from .forms import ScheduleBulkSelectForm

# ─── helpers ──────────────────────────────────────────────────────────────────

def is_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

staff_required = user_passes_test(is_staff, login_url='/dashboard/login/')


# ─── public views ─────────────────────────────────────────────────────────────

def landing_page(request):
    events        = Event.objects.filter(is_active=True).order_by('date')
    announcements = Announcement.objects.filter(is_published=True).order_by('-publish_date')[:5]
    speakers      = Speaker.objects.select_related('event').filter(event__is_active=True)
    sponsors      = Sponsor.objects.select_related('event').filter(event__is_active=True)
    schedule = ProgramSchedule.objects.select_related('event').filter(
        event__is_active=True
    ).order_by('event__id', 'time')

    try:
        site = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        site = None

    launch_date_iso = site.launch_date.isoformat() if site and site.launch_date else None

    return render(request, 'core/landing.html', {
        'events':         events,
        'announcements':  announcements,
        'speakers':       speakers,
        'sponsors':       sponsors,
        'schedule':       schedule,
        'site':           site,
        'launch_date_iso': launch_date_iso,
    })


from django.db import IntegrityError, transaction

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    is_hackathon = event.event_type == 'hackathon'

    registered = False
    saved_obj  = None
    event = get_object_or_404(Event, pk=pk, is_active=True)
    is_hackathon = event.event_type == 'hackathon'

    speakers = event.speakers.all()
    sponsors = event.sponsors.all()
    schedule = event.schedule_items.all()
    if request.method == 'POST':
        if is_hackathon:
            form = HackathonTeamForm(request.POST, event=event)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        team = form.save(commit=False)
                        team.event = event
                        team.save()

                        # Parse dynamic member fields: member_name[], member_email[], member_role[]
                        names  = request.POST.getlist('member_name')
                        emails = request.POST.getlist('member_email')
                        roles  = request.POST.getlist('member_role')
                        for n, e, r in zip(names, emails, roles):
                            if n.strip():
                                TeamMember.objects.create(team=team, name=n.strip(), email=e.strip(), role=r.strip())

                    registered = True
                    saved_obj  = team
                    form = HackathonTeamForm(event=event)
                except IntegrityError:
                    form.add_error('team_leader_email', 'This email is already registered for this event.')
        else:
            form = RegistrationForm(request.POST, event=event)
            if form.is_valid():
                try:
                    reg = form.save(commit=False)
                    reg.event = event
                    reg.save()
                    registered = True
                    saved_obj  = reg
                    form = RegistrationForm(event=event)
                except IntegrityError:
                    form.add_error('email', 'This email has already been registered for this event.')
    else:
        form = HackathonTeamForm(event=event) if is_hackathon else RegistrationForm(event=event)

    return render(request, 'core/event_detail.html', {
        'event': event,
        'form': form,
        'is_hackathon': is_hackathon,
        'registered': registered,
        'saved_obj': saved_obj,
        'speakers': speakers,
        'sponsors': sponsors,
        'schedule': schedule,
    })

# ─── dashboard auth ───────────────────────────────────────────────────────────

def dashboard_login(request):
    if is_staff(request.user):
        return redirect('dashboard_home')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user and is_staff(user):
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard_home'))
        messages.error(request, 'Invalid credentials or insufficient permissions.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ─── dashboard views ──────────────────────────────────────────────────────────

@staff_required
def dashboard_home(request):
    total_reg    = Registration.objects.count()
    total_events = Event.objects.count()
    total_ann    = Announcement.objects.filter(is_published=True).count()

    reg_by_event = (
        Registration.objects
        .values('event__title')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    recent_reg   = Registration.objects.select_related('event').order_by('-registered_at')[:8]
    recent_ann   = Announcement.objects.order_by('-created_at')[:5]
    upcoming     = Event.objects.filter(is_active=True, date__gte=timezone.now().date()).order_by('date')[:3]

    return render(request, 'dashboard/home.html', {
        'total_reg':    total_reg,
        'total_events': total_events,
        'total_ann':    total_ann,
        'reg_by_event': reg_by_event,
        'recent_reg':   recent_reg,
        'recent_ann':   recent_ann,
        'upcoming':     upcoming,
    })


# events
@staff_required
def dashboard_events(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'dashboard/events.html', {'events': events})


@staff_required
def dashboard_event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Event created successfully.')
        return redirect('dashboard_events')
    return render(request, 'dashboard/event_form.html', {'form': form, 'action': 'Create'})


@staff_required
def dashboard_event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form  = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Event updated successfully.')
        return redirect('dashboard_events')
    return render(request, 'dashboard/event_form.html', {'form': form, 'action': 'Edit', 'event': event})


@staff_required
def dashboard_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
    return redirect('dashboard_events')


# announcements
@staff_required
def dashboard_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'dashboard/announcements.html', {'announcements': announcements})


@staff_required
def dashboard_announcement_create(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Announcement created.')
        return redirect('dashboard_announcements')
    return render(request, 'dashboard/announcement_form.html', {'form': form, 'action': 'Create'})


@staff_required
def dashboard_announcement_edit(request, pk):
    ann  = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForm(request.POST or None, instance=ann)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Announcement updated.')
        return redirect('dashboard_announcements')
    return render(request, 'dashboard/announcement_form.html', {'form': form, 'action': 'Edit', 'announcement': ann})


@staff_required
def dashboard_announcement_delete(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        ann.delete()
        messages.success(request, 'Announcement deleted.')
    return redirect('dashboard_announcements')


@staff_required
def dashboard_registrations(request):
    event_id_raw = request.GET.get('event', '').strip()
    regs   = Registration.objects.select_related('event').order_by('-registered_at')
    teams  = HackathonTeam.objects.select_related('event').prefetch_related('members').order_by('-registered_at')
    events = Event.objects.all().order_by('title')

    selected_event = None
    if event_id_raw.isdigit():
        selected_event = int(event_id_raw)
        regs  = regs.filter(event_id=selected_event)
        teams = teams.filter(event_id=selected_event)

    return render(request, 'dashboard/registrations.html', {
        'registrations':  regs,
        'teams':          teams,
        'events':         events,
        'selected_event': selected_event,
    })

# speakers
@staff_required
def dashboard_speakers(request):
    speakers = Speaker.objects.select_related('event').all()
    return render(request, 'dashboard/speakers.html', {'speakers': speakers})


@staff_required
def dashboard_speaker_create(request):
    form = SpeakerForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Speaker added.')
        return redirect('dashboard_speakers')
    return render(request, 'dashboard/speaker_form.html', {'form': form, 'action': 'Add'})


@staff_required
def dashboard_speaker_edit(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    form = SpeakerForm(request.POST or None, request.FILES or None, instance=speaker)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Speaker updated.')
        return redirect('dashboard_speakers')
    return render(request, 'dashboard/speaker_form.html', {'form': form, 'action': 'Edit', 'speaker': speaker})


@staff_required
def dashboard_speaker_delete(request, pk):
    speaker = get_object_or_404(Speaker, pk=pk)
    if request.method == 'POST':
        speaker.delete()
        messages.success(request, 'Speaker removed.')
    return redirect('dashboard_speakers')


# sponsors
@staff_required
def dashboard_sponsors(request):
    sponsors = Sponsor.objects.select_related('event').all()
    return render(request, 'dashboard/sponsors.html', {'sponsors': sponsors})


@staff_required
def dashboard_sponsor_create(request):
    form = SponsorForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Sponsor added.')
        return redirect('dashboard_sponsors')
    return render(request, 'dashboard/sponsor_form.html', {'form': form, 'action': 'Add'})


@staff_required
def dashboard_sponsor_edit(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    form = SponsorForm(request.POST or None, request.FILES or None, instance=sponsor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Sponsor updated.')
        return redirect('dashboard_sponsors')
    return render(request, 'dashboard/sponsor_form.html', {'form': form, 'action': 'Edit', 'sponsor': sponsor})


@staff_required
def dashboard_sponsor_delete(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        sponsor.delete()
        messages.success(request, 'Sponsor removed.')
    return redirect('dashboard_sponsors')


# schedule
@staff_required
def dashboard_schedule(request):
    items = ProgramSchedule.objects.select_related('event').all()
    return render(request, 'dashboard/schedule.html', {'items': items})


@staff_required
def dashboard_schedule_create(request):
    form = ProgramScheduleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Schedule item added.')
        return redirect('dashboard_schedule')
    return render(request, 'dashboard/schedule_form.html', {'form': form, 'action': 'Add'})


@staff_required
def dashboard_schedule_edit(request, pk):
    item = get_object_or_404(ProgramSchedule, pk=pk)
    form = ProgramScheduleForm(request.POST or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Schedule item updated.')
        return redirect('dashboard_schedule')
    return render(request, 'dashboard/schedule_form.html', {'form': form, 'action': 'Edit', 'item': item})


@staff_required
def dashboard_schedule_delete(request, pk):
    item = get_object_or_404(ProgramSchedule, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Schedule item removed.')
    return redirect('dashboard_schedule')

@staff_required
def dashboard_schedule_bulk(request):
    select_form = ScheduleBulkSelectForm(request.GET or None)
    event = None

    if request.method == 'GET' and request.GET.get('event'):
        select_form = ScheduleBulkSelectForm(request.GET)
        if select_form.is_valid():
            event = select_form.cleaned_data['event']

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        times        = request.POST.getlist('item_time')
        activities   = request.POST.getlist('item_activity')
        descriptions = request.POST.getlist('item_description')

        created_count = 0
        with transaction.atomic():
            for i, (t, a, d) in enumerate(zip(times, activities, descriptions)):
                if a.strip() and t.strip():
                    ProgramSchedule.objects.create(
                        event=event,
                        time=t,
                        activity=a.strip(),
                        description=d.strip(),
                        order=i,
                    )
                    created_count += 1

        if created_count:
            messages.success(request, f'{created_count} schedule item(s) added to {event.title}.')
        else:
            messages.error(request, 'No valid rows were submitted — each row needs a time and an activity.')
        return redirect('dashboard_schedule')

    existing_items = event.schedule_items.all() if event else []

    return render(request, 'dashboard/schedule_bulk.html', {
        'select_form':   select_form,
        'event':         event,
        'existing_items': existing_items,
    })