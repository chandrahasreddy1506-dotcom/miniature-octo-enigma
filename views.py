from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, RegisterForm
from .models import Issue, UserProfile


def home(request):
    issues = Issue.objects.all().order_by("-created_at")

    return render(
        request,
        "issues/home.html",
        {"issues": issues}
    )


def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.save()

            return redirect("issue_detail", issue_id=issue.id)

    else:
        form = CommentForm()

    comments = issue.comments.all().order_by("-created_at")

    return render(
        request,
        "issues/issue_detail.html",
        {
            "issue": issue,
            "form": form,
            "comments": comments,
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            selected_region = form.cleaned_data["region"]

            UserProfile.objects.create(
                user=user,
                region=selected_region,
                city=selected_region.city,
                community=selected_region.community,
            )

            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "issues/register.html",
        {"form": form}
    )


def logout_user(request):
    logout(request)
    return redirect("home")