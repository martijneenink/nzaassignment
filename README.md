# What is this

This is my solution of the NZa programming assignment. If you don't know what
this means, you're probably in the wrong place ;-).

# Instructions for use

What do you need to run this software?

1. git
2. Docker and Docker Compose (an installation of Docker Desktop will suffice)

To run the software and see the result, do the following:

1. Clone the repository to a folder on your local machine
2. From the folder, run the following command:

`$ docker compose up --build --quiet-pull --no-log-prefix --attach app`

This will initialize two docker containers with a MySQL database and python
environment, respectively. This will take a while. After initialization is
done, a table with ISO country codes and country names will be printed.

To run the software again, first execute `$ docker compose down` and then repeat
step 2.
