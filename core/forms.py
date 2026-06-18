from django import forms
from .models import Registration, Event, Announcement, HackathonTeam


class RegistrationForm(forms.ModelForm):
    class Meta:
        model  = Registration
        fields = ['full_name', 'email', 'phone', 'organization', 'area_of_interest']
        widgets = {
            'full_name':        forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email':            forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone':            forms.TextInput(attrs={'placeholder': '+254 700 000 000'}),
            'organization':     forms.TextInput(attrs={'placeholder': 'Company / School / Individual'}),
            'area_of_interest': forms.TextInput(attrs={'placeholder': 'e.g. AI, Fintech, Health'}),
        }

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        if event and event.event_type != 'townhall':
            self.fields.pop('area_of_interest', None)

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.event and Registration.objects.filter(event=self.event, email__iexact=email).exists():
            raise forms.ValidationError("This email has already been registered for this event.")
        return email


class HackathonTeamForm(forms.ModelForm):
    class Meta:
        model  = HackathonTeam
        fields = ['team_name', 'team_leader_name', 'team_leader_email', 'team_leader_phone',
                  'skills', 'project_category']
        widgets = {
            'team_name':         forms.TextInput(attrs={'placeholder': 'Your team name'}),
            'team_leader_name':  forms.TextInput(attrs={'placeholder': 'Team leader full name'}),
            'team_leader_email': forms.EmailInput(attrs={'placeholder': 'leader@email.com'}),
            'team_leader_phone': forms.TextInput(attrs={'placeholder': '+254 700 000 000'}),
            'skills':            forms.Textarea(attrs={'placeholder': 'e.g. Python, UI/UX, Data Science', 'rows': 2}),
            'project_category':  forms.TextInput(attrs={'placeholder': 'e.g. AgriTech, EdTech'}),
        }

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def clean_team_leader_email(self):
        email = self.cleaned_data['team_leader_email']
        if self.event and HackathonTeam.objects.filter(event=self.event, team_leader_email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered as a team leader for this event.")
        return email


class EventForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = ['title', 'event_type', 'date', 'time', 'venue', 'description',
                  'theme', 'prize_info', 'poster', 'is_active']
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'Event title'}),
            'venue':       forms.TextInput(attrs={'placeholder': 'Venue name and address'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the event...'}),
            'theme':       forms.TextInput(attrs={'placeholder': 'Hackathon theme (optional)'}),
            'prize_info':  forms.Textarea(attrs={'rows': 3, 'placeholder': 'Prize details (optional)'}),
            'date':        forms.DateInput(attrs={'type': 'date'}),
            'time':        forms.TimeInput(attrs={'type': 'time'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model  = Announcement
        fields = ['title', 'content', 'category', 'event', 'is_published', 'publish_date']
        widgets = {
            'title':        forms.TextInput(attrs={'placeholder': 'Announcement title'}),
            'content':      forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your announcement...'}),
            'publish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

from .models import Speaker, Sponsor, ProgramSchedule

class SpeakerForm(forms.ModelForm):
    class Meta:
        model  = Speaker
        fields = ['event', 'name', 'position', 'biography', 'photo', 'order']
        widgets = {
            'name':      forms.TextInput(attrs={'placeholder': 'Full name'}),
            'position':  forms.TextInput(attrs={'placeholder': 'e.g. CEO, TechCorp'}),
            'biography': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Short biography...'}),
            'order':     forms.NumberInput(attrs={'min': 0}),
        }


class SponsorForm(forms.ModelForm):
    class Meta:
        model  = Sponsor
        fields = ['event', 'name', 'logo', 'website_url', 'tier', 'order']
        widgets = {
            'name':        forms.TextInput(attrs={'placeholder': 'Sponsor / partner name'}),
            'website_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'order':       forms.NumberInput(attrs={'min': 0}),
        }


class ProgramScheduleForm(forms.ModelForm):
    class Meta:
        model  = ProgramSchedule
        fields = ['event', 'time', 'activity', 'description', 'order']
        widgets = {
            'time':        forms.TimeInput(attrs={'type': 'time'}),
            'activity':    forms.TextInput(attrs={'placeholder': 'e.g. Opening Ceremony'}),
            'description': forms.TextInput(attrs={'placeholder': 'Optional short note'}),
            'order':       forms.NumberInput(attrs={'min': 0}),
        }

class ScheduleBulkSelectForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all().order_by('date', 'title'),
        empty_label="— Select an event —",
        widget=forms.Select(attrs={'onchange': 'this.form.submit()'})
    )