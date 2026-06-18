"""
Management command: python manage.py seed_phase1
Populates the database with sample Phase 1 data for development.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta
from core.models import Event, SiteSettings


class Command(BaseCommand):
    help = 'Seed the database with Phase 1 demo data'

    def handle(self, *args, **options):
        # Site Settings
        settings, _ = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'hub_name': 'Digital Hub',
                'tagline': 'Innovate. Connect. Transform. — The future starts here.',
                'launch_date': timezone.now() + timedelta(days=30),
                'about_mission': (
                    'To empower individuals and organizations by providing world-class '
                    'digital infrastructure, mentorship, and collaborative opportunities '
                    'that drive sustainable innovation and growth.'
                ),
                'about_vision': (
                    'To become the leading technology and innovation hub that catalyses '
                    'economic transformation and positions our region as a global digital powerhouse.'
                ),
                'about_objectives': (
                    'Foster entrepreneurship, provide access to emerging technologies, '
                    'support startups, and create pathways to digital careers for youth and '
                    'professionals alike.'
                ),
                'about_impact': (
                    'Generate employment, accelerate startup growth, build digital skills '
                    'across thousands of individuals, and attract investment into the local '
                    'technology ecosystem.'
                ),
                'contact_email': 'info@digitalhub.co.ke',
                'contact_phone': '+254 700 000 000',
                'contact_address': 'Digital Hub Campus, Innovation Drive, Nairobi, Kenya',
            }
        )
        self.stdout.write(self.style.SUCCESS('✔ SiteSettings seeded'))

        today = date.today()

        events = [
            {
                'event_type': 'townhall',
                'title': 'Digital Hub Town Hall Meeting',
                'date': today + timedelta(days=7),
                'time': time(9, 0),
                'venue': 'Community Hall, Innovation Drive, Nairobi',
                'description': (
                    'Community engagement session where stakeholders discuss plans, '
                    'ask questions, and share ideas ahead of the official launch.'
                ),
            },
            {
                'event_type': 'launch',
                'title': 'Official Digital Hub Launch',
                'date': today + timedelta(days=30),
                'time': time(8, 0),
                'venue': 'Digital Hub Campus, Innovation Drive, Nairobi',
                'description': 'The grand opening ceremony of the Digital Hub.',
            },
            {
                'event_type': 'hackathon',
                'title': 'Digital Hub Inaugural Hackathon',
                'date': today + timedelta(days=30),
                'time': time(13, 0),
                'venue': 'Digital Hub Campus — Innovation Labs',
                'theme': 'Tech for Community Impact',
                'prize_info': 'Grand Prize: KES 100,000 | Runner-Up: KES 50,000 | 3rd Place: KES 25,000',
            },
        ]

        for ev in events:
            obj, created = Event.objects.update_or_create(
                event_type=ev['event_type'], defaults=ev
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'✔ {action} event: {obj.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Phase 1 seed data loaded successfully!'))
        self.stdout.write('   Run: python manage.py runserver')
        self.stdout.write('   Visit: http://127.0.0.1:8000/')
