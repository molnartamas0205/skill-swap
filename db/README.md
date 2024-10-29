# DB init readme

## How to set-up the database:
1. Download and install Docker and Docker-compose. [link](https://www.docker.com/products/docker-desktop/)
2. Run the docker-compose.yml file with: `docker-compose up -d` from the same directory as the .yml file

## How to check if the database runs correctly:
1. Run `docker exec -it [container_id] bash`  
Note: You can copy paste the container id from Docker Desktop.  
If you encounter `the input device is not a TTY.  If you are using mintty, try prefixing the command with 'winpty'` then put `winpty` before the `docker exec` command.
2. Run  `psql -U django_user -d django_db`
3. Run `select * from users;`
Note: The `;` character is MANDATORY.
4. If you see 2 rows: john_doe and jane_smith then the docker runs correctly, otherwise contact Mate Kristof.