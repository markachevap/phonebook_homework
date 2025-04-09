## Phonebook

Phonebook was my homework which helped me to gather my knowledge about docker and project architecture. It is simple and it exists only to train my skills. 
There are not a lot of functions: create, edit, find and delete a contact. My program also punishes user for "bad" inputs: null in the name or phone number field, attempts to create 2 or more contacts with same phone number, wrong format of number. 
If user inputs data incorrectly, program erases all data in contact and user will have to write all information again. In my opinion that is fair.
### It was built with...
• HTML<br/>
• CSS<br/>
• Python + Flask<br/>
• Docker<br/>
• PostgreSQL<br/>
• Nginx<br/>
In addition, there is pgAdmin4 in the container, but it is unnesessary, it was only the part of teacher's task to get high score. 

## Installation instructions

### installation
1. Clone repository<br/>
git clone https://github.com/markachevap/phonebook_homework.git<br/>
cd phonebook_homework<br/>
2. Build the project via Docker<br/>
docker-compose up --build<br/>
3. Access at: http://localhost:8080<br/>
