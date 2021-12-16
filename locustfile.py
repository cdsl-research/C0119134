from locust import FastHttpUser, task
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
class MyUser(FastHttpUser):
    @task
    def index(self):
        response = self.client.get("/ubuntu/")