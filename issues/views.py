import csv
import subprocess
from pathlib import Path
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Issue
from .forms import IssueForm


def register_view(request):
    """
    Citizen registration endpoint for creating new accounts.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """
    Main civic dashboard: displays KPIs, handles complaint submissions,
    and supports complaint tracking and CSV export.
    """
    # 1. Handle CSV Export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="civic_issues_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Tracking ID', 'Title', 'Department', 'Location', 'Status', 'Citizen Name', 'Created At'])
        for issue in Issue.objects.all().order_by('-created_at'):
            writer.writerow([
                issue.tracking_id,
                issue.title,
                issue.department,
                issue.location,
                issue.status,
                issue.citizen_name,
                issue.created_at.strftime("%Y-%m-%d %H:%M")
            ])
        return response

    # 2. Handle Modal Grievance Submission
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.citizen_name = request.user.username if request.user.is_authenticated else 'Anonymous'
            issue.save()
            return redirect('dashboard')
    else:
        form = IssueForm()

    # 3. Handle Issue Tracking Search
    track_id = request.GET.get('track', '').strip()
    tracked_issue = None
    if track_id:
        tracked_issue = Issue.objects.filter(tracking_id__iexact=track_id).first()

    # 4. Metrics & Issue Listing
    issues = Issue.objects.all().order_by('-created_at')
    total_issues = issues.count()
    in_progress = issues.filter(status='In Progress').count()
    resolved = issues.filter(status='Resolved').count()
    submitted = issues.filter(status='Submitted').count()

    context = {
        'form': form,
        'issues': issues,
        'total_issues': total_issues,
        'in_progress': in_progress,
        'resolved': resolved,
        'submitted': submitted,
        'tracked_issue': tracked_issue,
    }
    return render(request, 'issues/dashboard.html', context)


@login_required
def export_csv(request):
    """Direct URL endpoint for downloading the civic grievances CSV export."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="civic_issues_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Tracking ID', 'Title', 'Department', 'Location', 'Status', 'Citizen Name', 'Created At'])
    for issue in Issue.objects.all().order_by('-created_at'):
        writer.writerow([
            issue.tracking_id,
            issue.title,
            issue.department,
            issue.location,
            issue.status,
            issue.citizen_name,
            issue.created_at.strftime("%Y-%m-%d %H:%M")
        ])
    return response


@csrf_exempt
def deploy_webhook(request):
    """Secure endpoint triggered by GitHub Actions CD to pull code, migrate, and reload."""
    token = request.GET.get("token")
    if token != "TalkAndSolveDeployKey2026":
        return HttpResponseForbidden("Unauthorized")

    # 1. Pull latest code from GitHub
    pull_proc = subprocess.run(
        ["git", "pull", "origin", "main"],
        cwd=settings.BASE_DIR,
        capture_output=True,
        text=True
    )

    # 2. Run database migrations
    call_command("migrate")

    # 3. Trigger immediate webapp reload on PythonAnywhere
    wsgi_file = Path("/var/www/chandu1_pythonanywhere_com_wsgi.py")
    if wsgi_file.exists():
        wsgi_file.touch()

    return HttpResponse(
        f"Deployment output:\n{pull_proc.stdout}\nReload triggered via WSGI touch.",
        content_type="text/plain"
    )


# Backward compatibility aliases
issue_dashboard = dashboard
export_issues_csv = export_csv