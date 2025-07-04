# pyGFAccess microservice for pyGameFlix

### My Development Setup

- Install Python 3.13.4
- Install pipenv
- Create virtual environment
    - > $ pipenv install --python /path/to/python3
- Create .env file with SQLALCHEMY_DATABASE_URI variable set to PostgreSQL database
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
