import os

from locust import HttpUser, between, task


class TalkAndSolveUser(HttpUser):
    wait_time = between(1, 3)
    host = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    @task(4)
    def home(self):
        self.client.get("/")

    @task(2)
    def login(self):
        self.client.get("/login/")

    @task(2)
    def register(self):
        self.client.get("/register/")

    @task(1)
    def issue_detail(self):
        self.client.get("/issues/1/")
