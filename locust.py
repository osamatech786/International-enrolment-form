from locust import HttpUser,task,between 

class AppUser(HttpUser):
	wait_time = between(2,5)

	# Endpoint
	@task
	def home_page(self):
		self.client.get("/")

# locust -f locust.py
# http://localhost:8089/
