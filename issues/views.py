import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Issue
from .forms import IssueForm

def sanitize_csv_cell(value):
    val_str = str(value or '')
    if val_str.startswith(('=', '+', '-', '@', '\t', '\r')):
        return f"'{val_str}"
    return val_str

@login_required
def issue_dashboard(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.citizen_name = request.user.username
            issue.status = 'Submitted'
            issue.save()
            return redirect('dashboard')
    else:
        form = IssueForm()

    issues = Issue.objects.all().order_by('-created_at')

    total_count = issues.count()
    submitted_count = issues.filter(status__iexact='Submitted').count()
    in_progress_count = issues.filter(status__iexact='In Progress').count()
    resolved_count = issues.filter(status__iexact='Resolved').count()

    search_query = request.GET.get('track_id', '').strip()[:20]
    tracked_issue = None
    if search_query:
        tracked_issue = Issue.objects.filter(tracking_id__iexact=search_query).first()

    context = {
        'issues': issues,
        'form': form,
        'total_count': total_count,
        'submitted_count': submitted_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'tracked_issue': tracked_issue,
        'search_query': search_query,
    }
    return render(request, 'issues/dashboard.html', context)

@login_required
def export_issues_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="talk_and_solve_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Tracking ID', 'Title', 'Department', 'Location', 'Status', 'Date Reported'])

    for issue in Issue.objects.all().order_by('-created_at'):
        writer.writerow([
            sanitize_csv_cell(issue.tracking_id),
            sanitize_csv_cell(issue.title),
            sanitize_csv_cell(issue.department),
            sanitize_csv_cell(issue.location),
            sanitize_csv_cell(issue.status),
            issue.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    return response

def register_view(request):
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