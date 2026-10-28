from django.contrib.auth.models import User
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse

from .models import Category, Comment, Issue, Region, UserProfile


@override_settings(SECURE_SSL_REDIRECT=False)
class IssueFlowTests(TestCase):
	def setUp(self):
		self.region = Region.objects.create(
			city="Nairobi",
			community="Westlands",
			is_active=True,
		)
		self.category = Category.objects.create(name="Roads")
		self.issue = Issue.objects.create(
			title="Pothole near market",
			description="Large pothole causing traffic delays.",
			category=self.category,
			region=self.region,
			city=self.region.city,
			community=self.region.community,
			status=Issue.Status.OPEN,
		)

	def test_home_page_lists_issues(self):
		response = self.client.get(reverse("home"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.issue.title)

	def test_issue_detail_page_renders(self):
		response = self.client.get(reverse("issue_detail", args=[self.issue.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.issue.description)

	def test_comment_submission_creates_comment(self):
		response = self.client.post(
			reverse("issue_detail", args=[self.issue.id]),
			{
				"name": "Alice",
				"message": "I can coordinate with local council.",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(
			Comment.objects.filter(
				issue=self.issue,
				name="Alice",
			).exists()
		)


@override_settings(SECURE_SSL_REDIRECT=False)
class AuthFlowTests(TestCase):
	def setUp(self):
		self.region = Region.objects.create(
			city="Nairobi",
			community="Kilimani",
			is_active=True,
		)

	def test_register_creates_user_and_profile(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "new_user",
				"email": "new_user@example.com",
				"region": self.region.id,
				"password1": "StrongPass12345!",
				"password2": "StrongPass12345!",
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("home"))
		self.assertTrue(User.objects.filter(username="new_user").exists())

		profile = UserProfile.objects.get(user__username="new_user")
		self.assertEqual(profile.region, self.region)
		self.assertEqual(profile.city, self.region.city)
		self.assertEqual(profile.community, self.region.community)

	def test_login_and_logout_redirects_home(self):
		User.objects.create_user(
			username="tester",
			email="tester@example.com",
			password="StrongPass12345!",
		)

		login_response = self.client.post(
			reverse("login"),
			{
				"username": "tester",
				"password": "StrongPass12345!",
			},
		)

		self.assertEqual(login_response.status_code, 302)
		self.assertEqual(login_response.url, reverse("home"))

		logout_response = self.client.get(reverse("logout"))
		self.assertEqual(logout_response.status_code, 302)
		self.assertEqual(logout_response.url, reverse("home"))
