#! /usr/bin/python
from locust import HttpLocust, TaskSet, task

import event_generator


class UserBehavior(TaskSet):
    # Wait .5 to 1 second in between task executions
    min_wait = 500
    max_wait = 1000

    @task
    def browse(self):
        # Assumes NiFi's ListenHTTP endpoint
        self.locust.client.post('/contentListener', json=event_generator.create_event())


class WebsiteUser(HttpLocust):
    task_set = UserBehavior