# pyGFAccess microservice for pyGameFlix

### My Development Setup

- Install Python 3.13.4
- Install pipenv
- Create virtual environment
    - > $ pipenv install --python /path/to/python3
- Create .env file with SQLALCHEMY_DATABASE_URI variable set to application database
    - 'SQLALCHEMY_DATABASE_URI='postgresql://db_user:db_password@ip.add.re.ss/db_name'
        - db_dialect: mysql or postgresql
        - db_user: user for the database
        - db_password: password for the above mentioned db_user
        - db_name: name of the database
        - ip.add.re.ss: ip address of the database server
- Launch virtual environment
    - > $ pipenv shell
- Start application
    - > $ python3 access.py 

### Provides 4 endpoints use for authentication and account services

- GET /: utilizes the index function that just provides simple documentation of the microservice endpoints
    - Required data: None
    - Returns: a JSON object with this information as documentation
- POST /login: utilizes the login function which validates the user and provides user profile data
    - Required data: a JSON object with users email and encrypted password
    - Returns: a JSON object with users profile data
- GET /logout: utilizes the logout function which terminates the end user session within pyGameFlix
    - Required data: TBD
    - Returns: TBD
- POST /register: utilizes the register function that receives the provided end user profile information and password and populates the users table within the pyGameFlix database
    - Required data: a JSON object with the end users profile information and password
    - Returns: a JSON object with the end users profile information

### Instructions for QA (Instructor) Testing application container

- Clone repository
- Create 'keys' directory
    - > $ mkdir keys
- Change to 'keys' directory and create pki pair
    - > $ openssl req -x509 -nodes -newkey rsa:4096 -keyout private_key.pem -out public_key.pem -subj "/CN=CommonName"
- Create .env file with SQLALCHEMY_DATABASE_URI variable set to application database
    - 'SQLALCHEMY_DATABASE_URI='db_dialect://db_user:db_password@ip.add.re.ss/db_name'
        - db_dialect: mysql or postgresql
        - db_user: user for the database
        - db_password: password for the above mentioned db_user
        - db_name: name of the database
        - ip.add.re.ss: ip address of the database server
- Build docker image
    - > $ docker build -t docker_tag .
- Verify Image ID
    - > $ docker image ls
- Launch docker image
    - > $ docker run -p 5001:5001 -d ImageID

### JSON for testing

- Built-in documentation
    - http://ip.add.re.ss:5001
- Create user
    - http://ip.add.re.ss:5001/register 
    - {
      "first_name": "Max",
      "last_name": "Yeomans",
      "email": "my0106@proton.me",
      "address": "around the corner",
      "city": "Seffner",
      "state": "Florida",
      "zip_code": "33584",
      "password": "$2b$12$ZYuzjqJzR3dj2gzOYkPCwuzKtJLP1oQCPJJTgVCyPfbl2sfYgkBoO",
      "subscription_id": 2,
      "access_level": 99
    }
- User login
    - http://ip.add.re.ss:5001/login 
    - {
      "email": ""my0106@proton.me,
      "password": "$2b$12$ZYuzjqJzR3dj2gzOYkPCwuzKtJLP1oQCPJJTgVCyPfbl2sfYgkBoO"
    }