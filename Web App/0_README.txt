

TODO:

1. Deploy MySQL DB

CREATE DATABASE school;

USE school;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    student_id INT UNIQUE,
    math INT,
    english INT,
    physics INT,
    chemistry INT,
    spanish INT
);


2. Load lots of data into the database [python3 ./generate_students_record.py 10000]
3. Run a python web app (may be flask app) to retrieve
   data from the database and display.
4. Deploy a metrics server and HPA for auto scaling.
5. Deploy the webapp
6. Run mutiple requests to the web app and check the 
   the webapp pods scaling up and down


# Create a container image for the webapp
# by saving the ubuntu image
docker commit a59e8d97026a webapp


Security Improvement:
=====================

1. TLS security for API
2. Add vault for storing mysql username and password


####

IMPORTANT NOTES:
================

Using service for PODs communication.

 Once a POD has a service deployed, connect the POD using <service-name>.<namespace>.svc,cluster.local
Below connection fron one POD to another POD.

(venv) root@webapi-deployment-694984b79-fkhxx:/app# ping mysql.mysql-webapp.svc.cluster.local
PING mysql.mysql-webapp.svc.cluster.local (10.244.0.12) 56(84) bytes of data.
64 bytes from 10-244-0-12.mysql.mysql-webapp.svc.cluster.local (10.244.0.12): icmp_seq=1 ttl=64 time=0.055 ms
64 bytes from 10-244-0-12.mysql.mysql-webapp.svc.cluster.local (10.244.0.12): icmp_seq=2 ttl=64 time=0.077 ms
64 bytes from 10-244-0-12.mysql.mysql-webapp.svc.cluster.local (10.244.0.12): icmp_seq=3 ttl=64 time=0.091 ms
64 bytes from 10-244-0-12.mysql.mysql-webapp.svc.cluster.local (10.244.0.12): icmp_seq=4 ttl=64 time=0.086 ms
^C
--- mysql.mysql-webapp.svc.cluster.local ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3110ms
rtt min/avg/max/mdev = 0.055/0.077/0.091/0.013 ms
(venv) root@webapi-deployment-694984b79-fkhxx:/app#


=================================================================================================================================
