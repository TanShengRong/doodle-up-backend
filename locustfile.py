from locust import HttpUser, TaskSet, task, between


class UserTasks(TaskSet):
    email = "pytest@gmail.com"
    password = "123456"

    @task
    def get_all_content(self):
        self.client.get("/content/all")

    @task
    def post_sign_in(self):
        self.client.post("/signin", {
            "email": self.email, 
            "password": self.password
        })


class FrontendApiCall(HttpUser):
    """
    User class that does requests to the locust web server running on localhost
    """

    host = "http://0.0.0.0:5000/"
    wait_time = between(2, 5)
    tasks = [UserTasks]