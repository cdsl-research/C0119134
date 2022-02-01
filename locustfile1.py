from locust import FastHttpUser, task, between
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
class MyUser(FastHttpUser):
    @task
    def index(self):
        response = self.client.get("/ubuntu/")
        wait_time = between(1, 5)
        response = self.client.get("/ubuntu/")
        wait_time = between(1, 5)
        response = self.client.get("/ubuntu/")


