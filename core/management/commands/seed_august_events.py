"""
Management command: python manage.py seed_august_events
Creates 3 events (Town Hall, Launch, Hackathon) in August with
fictional speakers and sponsors attached to each.
"""
from datetime import date, time
from django.core.management.base import BaseCommand
from core.models import Event, Speaker, Sponsor


class Command(BaseCommand):
    help = 'Seed August events with fictional speakers and sponsors'

    def handle(self, *args, **options):
        year = date.today().year
        if date.today().month >= 8:
            year += 1  # push to next year if August has already passed

        # ── EVENTS ──────────────────────────────────────────────
        townhall, _ = Event.objects.update_or_create(
            title="Digital Hub Town Hall Meeting",
            event_type='townhall',
            defaults={
                'date': date(year, 8, 5),
                'time': time(9, 0),
                'venue': "Hub Community Hall, Innovation Drive, Nairobi",
                'description': (
                    "An open community conversation ahead of launch — share your "
                    "expectations, ask questions, and help shape the Hub's first year."
                ),
                'is_active': True,
            }
        )

        launch, _ = Event.objects.update_or_create(
            title="Official Digital Hub Launch",
            event_type='launch',
            defaults={
                'date': date(year, 8, 22),
                'time': time(9, 0),
                'venue': "Digital Hub Campus, Innovation Drive, Nairobi",
                'description': (
                    "The official opening of the Digital Hub — keynotes, a campus tour, "
                    "and networking with the wider innovation community."
                ),
                'is_active': True,
            }
        )

        hackathon, _ = Event.objects.update_or_create(
            title="Digital Hub Inaugural Hackathon",
            event_type='hackathon',
            defaults={
                'date': date(year, 8, 22),
                'time': time(13, 0),
                'venue': "Digital Hub Campus — Innovation Labs",
                'theme': "Tech for Community Impact",
                'prize_info': "1st: KES 150,000 | 2nd: KES 80,000 | 3rd: KES 40,000",
                'description': (
                    "A 24-hour build challenge for developers, designers, and "
                    "entrepreneurs solving real problems for local communities."
                ),
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS(
            f'✔ Events created/updated for {year}: Town Hall (Aug 5), '
            f'Launch & Hackathon (Aug 22)'
        ))

        # ── SPEAKERS ────────────────────────────────────────────
        Speaker.objects.filter(event__in=[townhall, launch, hackathon]).delete()

        speakers_data = [
            (townhall, "Wanjiru Kamau", "Community Programs Lead, Mwangaza Foundation",
             "Wanjiru has spent a decade designing grassroots tech literacy programs across "
             "Kenya, helping over 20,000 young people access their first coding lessons.", 0),
            (townhall, "Brian Otieno", "Founder, JengaTech Hub",
             "Brian founded one of Nairobi's earliest co-working spaces for student developers "
             "and now advises county governments on digital inclusion strategy.", 1),

            (launch, "Dr. Amina Hassan", "Chief Innovation Officer, Pwani Digital Systems",
             "Dr. Hassan leads enterprise innovation strategy across East Africa and is a "
             "frequent speaker on public-private digital transformation partnerships.", 0),
            (launch, "Samuel Mwangi", "CEO, Baraka Cloud Solutions",
             "Samuel has built and scaled three startups in the fintech and logistics space, "
             "with a focus on solutions designed for the East African market.", 1),
            (launch, "Grace Nyambura", "Director of Partnerships, Uzima Innovation Trust",
             "Grace works at the intersection of philanthropy and technology, channeling "
             "funding toward youth-led innovation hubs across the region.", 2),

            (hackathon, "Kevin Ochieng", "Lead Mentor & Senior Engineer, Simba Code Labs",
             "Kevin mentors hackathon teams across East Africa and has judged over 30 "
             "innovation competitions in the last five years.", 0),
            (hackathon, "Faith Wairimu", "Product Design Lead, Tumaini Works",
             "Faith specializes in human-centered design for underserved communities and will "
             "be running the hackathon's design-thinking bootcamp session.", 1),
        ]

        for event, name, position, bio, order in speakers_data:
            Speaker.objects.create(
                event=event, name=name, position=position, biography=bio, order=order
            )

        self.stdout.write(self.style.SUCCESS(f'✔ {len(speakers_data)} speakers added'))

        # ── SPONSORS ────────────────────────────────────────────
        Sponsor.objects.filter(event__in=[townhall, launch, hackathon]).delete()

        sponsors_data = [
            (townhall, "Mwangaza Foundation", "partner", 0),
            (townhall, "JengaTech Hub", "partner", 1),

            (launch, "Pwani Digital Systems", "platinum", 0),
            (launch, "Baraka Cloud Solutions", "gold", 1),
            (launch, "Uzima Innovation Trust", "gold", 2),
            (launch, "Tembo Capital Partners", "silver", 3),

            (hackathon, "Simba Code Labs", "platinum", 0),
            (hackathon, "Tumaini Works", "gold", 1),
            (hackathon, "Nuru Telecom Foundation", "silver", 2),
        ]

        for event, name, tier, order in sponsors_data:
            Sponsor.objects.create(event=event, name=name, tier=tier, order=order)

        self.stdout.write(self.style.SUCCESS(f'✔ {len(sponsors_data)} sponsors added'))
        self.stdout.write(self.style.SUCCESS('\n✅ August seed complete. Visit your landing page to view.'))