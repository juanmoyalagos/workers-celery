from locust import HttpUser, task
from random import randint,seed
seed(1)
class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.post("http://app:8000/job", json={"number": randint(1, 10000000)})
