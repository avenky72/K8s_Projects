# K8s_Projects
Repo containing Kubernetes projects that show my growth and learning

Steps:

First dockerize the webapp using the Docerfile

Push the image to docker hub repository

Deploy MySQL

kubectl apply -f mysql8-deployment.yaml

Deploy WebApp image built and pushed to dockerhub

kubectl apply -f webapp-deployment.yaml

Check both deployment:

![image](https://github.com/user-attachments/assets/c7708f78-7d35-43c9-9a20-87282b5f73b0)

Now the reployment is completed.


Next Steps to do port forwarding for both MySQL and Webapp deployment pods.

Now, load sample data into MySQL DB using generate_students_record.py script.

Now all set to call the flask based REST API in webapp POD.

Each curl call will call the webapp which will conect with the MySQL pod to collect data from the DB and display on the console.

The sample REST API commands are in the runtest script.
