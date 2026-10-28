import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from issues.models import Ward, Community, Issue, Comment, IssueStatusLog

def populate():
    print("🌱 Seeding Wards, Communities, Issues, and Audit Logs...")

    citizen_user, _ = User.objects.get_or_create(
        username='community_voice',
        defaults={'email': 'citizen@talkandsolve.org'}
    )
    if not citizen_user.has_usable_password():
        citizen_user.set_password('CommunityPass123!')
        citizen_user.save()

    resident_user, _ = User.objects.get_or_create(
        username='local_resident',
        defaults={'email': 'resident@talkandsolve.org'}
    )
    if not resident_user.has_usable_password():
        resident_user.set_password('CommunityPass123!')
        resident_user.save()

    official_user, _ = User.objects.get_or_create(
        username='ward_engineer',
        defaults={'email': 'official@talkandsolve.org', 'is_staff': True}
    )
    if not official_user.has_usable_password():
        official_user.set_password('CommunityPass123!')
        official_user.save()

    wards_data = [
        {'ward_number': 84, 'name': 'Hagadur', 'zone': 'Mahadevapura Zone'},
        {'ward_number': 85, 'name': 'Doddanekkundi', 'zone': 'Mahadevapura Zone'},
        {'ward_number': 112, 'name': 'Domlur', 'zone': 'East Zone'},
        {'ward_number': 150, 'name': 'Bellandur', 'zone': 'Mahadevapura Zone'},
    ]

    ward_objects = {}
    for w in wards_data:
        ward_obj, _ = Ward.objects.get_or_create(
            ward_number=w['ward_number'],
            defaults={'name': w['name'], 'zone': w['zone']}
        )
        ward_objects[w['ward_number']] = ward_obj

    communities_data = [
        {'name': 'Brookefield Layout RWA', 'ward': ward_objects[85], 'postal_code': '560037'},
        {'name': 'Kundalahalli Colony Welfare Association', 'ward': ward_objects[85], 'postal_code': '560037'},
        {'name': 'AECS Layout Sector A', 'ward': ward_objects[85], 'postal_code': '560037'},
        {'name': 'Palm Meadows Community', 'ward': ward_objects[84], 'postal_code': '560066'},
        {'name': 'Immadihalli Residents Forum', 'ward': ward_objects[84], 'postal_code': '560066'},
        {'name': 'Green Glen Layout Association', 'ward': ward_objects[150], 'postal_code': '560103'},
        {'name': 'Kasavanahalli Lake Community', 'ward': ward_objects[150], 'postal_code': '560035'},
        {'name': 'Domlur 2nd Stage Residents Association', 'ward': ward_objects[112], 'postal_code': '560071'},
    ]

    community_objects = {}
    for c in communities_data:
        comm_obj, _ = Community.objects.get_or_create(
            name=c['name'],
            defaults={'ward': c['ward'], 'postal_code': c['postal_code']}
        )
        community_objects[c['name']] = comm_obj

    sample_issues = [
        {
            "title": "Main drinking water pipeline rupture causing low water pressure",
            "category": "water",
            "community": community_objects['Brookefield Layout RWA'],
            "location": "5th Cross Road, Brookefield Avenue",
            "status": "in_progress",
            "upvotes": 47,
            "description": "Clean water gushing from an underground line rupture since morning. Adjoining residential blocks have lost pipeline pressure.",
            "author": citizen_user,
            "old_status": "reported",
            "comments": [
                (resident_user, "Water board maintenance squad arrived and turned off the valve. Excavation underway.")
            ]
        },
        {
            "title": "Severe potholes along main junction after monsoon showers",
            "category": "road",
            "community": community_objects['Kundalahalli Colony Welfare Association'],
            "location": "Kundalahalli Gate Junction, Service Lane",
            "status": "reported",
            "upvotes": 34,
            "description": "Multiple crater-sized potholes across both carriage lanes. Two-wheelers swerving into incoming traffic to avoid them.",
            "author": resident_user,
            "old_status": None,
            "comments": [
                (citizen_user, "Extremely dangerous at night due to poor lighting.")
            ]
        },
        {
            "title": "Overflowing commercial garbage bins near children's park",
            "category": "garbage",
            "community": community_objects['Green Glen Layout Association'],
            "location": "Sector 2 Park Perimeter Road",
            "status": "reported",
            "upvotes": 19,
            "description": "Municipal waste bins have overflowed onto the walkway. Stray dogs scattering garbage over the pedestrian path.",
            "author": citizen_user,
            "old_status": None,
            "comments": []
        },
        {
            "title": "Backed-up stormwater drain overflowing onto pedestrian footpath",
            "category": "sewage",
            "community": community_objects['AECS Layout Sector A'],
            "location": "12th Main Road, Opposite Community Hall",
            "status": "in_progress",
            "upvotes": 38,
            "description": "Culvert blockage has caused stagnant greywater spill across the walkway, emitting severe foul odors.",
            "author": resident_user,
            "old_status": "reported",
            "comments": [
                (citizen_user, "Sanitation desilting team has been dispatched with suction equipment.")
            ]
        },
        {
            "title": "Four consecutive streetlights dark on Outer Ring Access Lane",
            "category": "electricity",
            "community": community_objects['Palm Meadows Community'],
            "location": "Poles #14 to #18, East Boundary Road",
            "status": "resolved",
            "upvotes": 52,
            "description": "Streetlight array dark for four consecutive days. Complete blackout along the residential boundary wall.",
            "author": citizen_user,
            "old_status": "in_progress",
            "comments": [
                (resident_user, "Linemen replaced blown junction cables. Lights are fully operational.")
            ]
        },
        {
            "title": "Dangerous blind curve missing convex mirror and warning signage",
            "category": "traffic",
            "community": community_objects['Immadihalli Residents Forum'],
            "location": "Immadihalli Main Road Turn, Near School Gate",
            "status": "reported",
            "upvotes": 26,
            "description": "Vehicles speeding around this sharp blind turn cannot see pedestrians crossing. Urgently needs a convex mirror and speed calming bumps.",
            "author": resident_user,
            "old_status": None,
            "comments": []
        },
        {
            "title": "Uprooted tree branch obstructing pedestrian jogging pathway",
            "category": "parks",
            "community": community_objects['Kasavanahalli Lake Community'],
            "location": "Lake Perimeter Jogging Trail, North Marker 12",
            "status": "resolved",
            "upvotes": 31,
            "description": "Snapped branch completely blocked the cycle and jogging track after high winds.",
            "author": citizen_user,
            "old_status": "in_progress",
            "comments": [
                (resident_user, "Forestry and gardening team chopped and removed the branch this morning.")
            ]
        },
        {
            "title": "Stagnant pool in vacant plot causing heavy mosquito breeding",
            "category": "health",
            "community": community_objects['Domlur 2nd Stage Residents Association'],
            "location": "Plot 42, 4th Cross Road",
            "status": "in_progress",
            "upvotes": 29,
            "description": "Excavated basement site filled with stagnant water is serving as a rampant mosquito breeding cluster.",
            "author": resident_user,
            "old_status": "reported",
            "comments": [
                (citizen_user, "Health inspector issued a notice to the property owner to pump out the water and spray larvicide.")
            ]
        },
    ]

    for data in sample_issues:
        comments = data.pop("comments")
        old_status = data.pop("old_status")

        issue, _ = Issue.objects.get_or_create(
            title=data["title"],
            defaults=data
        )

        if not issue.comments.exists():
            for author_obj, content in comments:
                Comment.objects.create(issue=issue, author=author_obj, content=content)

        if old_status and not issue.status_logs.exists():
            IssueStatusLog.objects.create(
                issue=issue,
                changed_by=official_user,
                old_status=old_status,
                new_status=issue.status
            )

    print(f"✅ Seeding Complete: {Ward.objects.count()} Wards, {Community.objects.count()} Communities, and {Issue.objects.count()} Issues active.")

if __name__ == '__main__':
    populate()