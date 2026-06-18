from django.db import models


class Event(models.Model):
    EVENT_TYPES = [
        ('townhall', 'Town Hall Meeting'),
        ('launch', 'Official Launch Event'),
        ('hackathon', 'Hackathon'),
        ('other', 'Other'),
    ]
    event_type  = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    title       = models.CharField(max_length=200)
    date        = models.DateField()
    time        = models.TimeField()
    venue       = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    theme       = models.CharField(max_length=200, blank=True)
    prize_info  = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
    poster      = models.ImageField(upload_to='posters/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title


class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('general',  'General'),
        ('event',    'Event Update'),
        ('venue',    'Venue Change'),
        ('speaker',  'Speaker Announcement'),
        ('hackathon','Hackathon Update'),
        ('winner',   'Winner Announcement'),
    ]
    title        = models.CharField(max_length=200)
    content      = models.TextField()
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    event        = models.ForeignKey(
        Event, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='announcements'
    )

    class Meta:
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title


class Registration(models.Model):
    event            = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name        = models.CharField(max_length=200)
    email            = models.EmailField()
    phone            = models.CharField(max_length=50, blank=True)
    organization     = models.CharField(max_length=200, blank=True)
    area_of_interest = models.CharField(max_length=200, blank=True)
    registered_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        constraints = [
            models.UniqueConstraint(fields=['event', 'email'], name='unique_registration_per_event')
        ]

    def __str__(self):
        return f"{self.full_name} — {self.event.title}"


class SiteSettings(models.Model):
    hub_name        = models.CharField(max_length=200, default="Digital Hub")
    tagline         = models.CharField(max_length=300, default="Innovate. Connect. Transform.")
    launch_date     = models.DateTimeField(null=True, blank=True)
    about_mission   = models.TextField(blank=True)
    about_vision    = models.TextField(blank=True)
    about_objectives= models.TextField(blank=True)
    about_impact    = models.TextField(blank=True)
    contact_email   = models.EmailField(blank=True)
    contact_phone   = models.CharField(max_length=50, blank=True)
    contact_address = models.TextField(blank=True)
    twitter_url     = models.URLField(blank=True)
    facebook_url    = models.URLField(blank=True)
    instagram_url   = models.URLField(blank=True)
    linkedin_url    = models.URLField(blank=True)

    class Meta:
        verbose_name        = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

class HackathonTeam(models.Model):
    event             = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='hackathon_teams')
    team_name         = models.CharField(max_length=200)
    team_leader_name  = models.CharField(max_length=200)
    team_leader_email = models.EmailField()
    team_leader_phone = models.CharField(max_length=50, blank=True)
    skills            = models.TextField(blank=True)
    project_category  = models.CharField(max_length=200, blank=True)
    registered_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        constraints = [
            models.UniqueConstraint(fields=['event', 'team_leader_email'], name='unique_team_per_event')
        ]

    def __str__(self):
        return f"{self.team_name} ({self.event.title})"

class TeamMember(models.Model):
    team = models.ForeignKey(HackathonTeam, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Speaker(models.Model):
    event     = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    name      = models.CharField(max_length=200)
    position  = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    photo     = models.ImageField(upload_to='speakers/', blank=True, null=True)
    order     = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.event.title})"


class Sponsor(models.Model):
    TIER_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold',     'Gold'),
        ('silver',   'Silver'),
        ('partner',  'Partner'),
    ]
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sponsors')
    name        = models.CharField(max_length=200)
    logo        = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    website_url = models.URLField(blank=True)
    tier        = models.CharField(max_length=20, choices=TIER_CHOICES, default='partner')
    order       = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['tier', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.event.title})"


class ProgramSchedule(models.Model):
    event       = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule_items')
    time        = models.TimeField()
    activity    = models.CharField(max_length=300)
    description = models.CharField(max_length=400, blank=True)
    order       = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['order', 'time']

    def __str__(self):
        return f"{self.time.strftime('%H:%M')} — {self.activity} ({self.event.title})"