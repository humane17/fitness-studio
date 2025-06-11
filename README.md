**Fitness Studio Booking API**

A simple Booking API for a fictional fitness studio using Python's FastAPI framework.
Consists of three endpoints - GET /classes, POST /book, GET /bookings, GET /memory and GET /timezones/sample. (Last two only for testing.)


1. GET /classes
   Response contains a list of upcoming classes that users/clients can book using book api.
   Takes user_timezone as a query parameter which should be passed with values like - America/New_York etc..

   CURL -
   curl --location 'http://127.0.0.1:8000/classes?user_timezone=Australia%2FSydney'

2. POST /book
   Accepts a set of body parameters in request with regards to booking details so that users can book a class.
   Data sent in request is validated before returning a success or error response.

   CURL -
   curl --location 'http://127.0.0.1:8000/book' \
               --header 'Content-Type: application/json' \
               --data-raw '{"class_id" : 6,"client_name":"Archana", "client_email":"test@gmail.com","client_timezone":"Asia/Kolkata","slots_reqd": 3}'

   

3. GET /bookings
   Returns all the bookings made by a user.
   Takes email as a query parameter. User email used for booking should be passed here.

   CURL -
   curl --location 'http://127.0.0.1:8000/booking?email=test%40gmail.com'

4. GET /memory
   Returns all the in-memory data being used during testing.

   CURL -
   curl --location --request GET 'http://127.0.0.1:8000/memory' \
                   --header 'Content-Type: application/json' \
                   --data-raw '{ "class_id" : 6,"client_name":"Neena","client_email":"test@gmail.com","client_timezone":"Africa/Djibouti","slots_reqd": 2}'

 5. GET /timezones/sample
    Return some sample timezone values that can be used to test api 1 (GET /classes).  

    CURL -
    curl --location 'http://127.0.0.1:8000/timezones/sample'

**Local Development Setup** 
Git should be installed in your system for this to work.
Check if installed using git --version command in your cmd/terminal.

1. Clone this repository
   In a directory of your choice clone this repository using the below command.
   git clone https://github.com/humane17/fitness-studio.git
   
3. Setup a virtual environment and activate it in your machine using the below command.
   python -m venv venv
   source venv/bin/activate   (# On Windows: venv\Scripts\activate)

4. Install Dependencies from requirements.txt file within codebase folder using below command.
   pip install -r requirements.txt

5. Run the application using uvicorn which is an in-built Fastapi server. To start the project type the below command in your terminal.
   uvicorn codebase.main:app --reload  (--reload to be used only in developer environment)

6. Once the server has started successfully you can open the below url in any browser to test it.
   Swagger UI: http://localhost:8000/docs
   
   

