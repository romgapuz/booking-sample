Both:

GET /user/<id> - Get user by ID
PUT /user/<id> - Update user
  - first_name
  - last_name
  - username
  - password
  - email
  - address
  - phone_no
  - registration_id
GET /booking/<id> - Get booking by ID
PUT /booking/<id> - Update booking
  - booking_date
  - booking_time
  - details
  - address
  - is_taken
  - is_done

Worker:

POST /worker/login - Login as worker
  - username
  - password
GET /worker/<id>/booking - Get bookings by worker ID
GET /worker/<id>/booking?is_taken=1 - Get bookings by worker ID
GET /worker/<id>/feedback - Get feedback by worker ID
GET /booking/available - Get available bookings
GET /booking/available?worker_id=<id> - Get available bookings for a worker considering the services he cater
GET /booking/taken?worker_id = Get taken booking by worker ID
POST /booking/<id>/request - Create request to a booking
  - booking_date
  - booking_time
  - details
  - worker_id
  
Customer:

POST /customer/login - Login as customer
  - username
  - password
POST /register - Register as customer
  - first_name
  - last_name
  - username
  - password
  - email
  - address
  - phone_no
POST /customer/<id>/verify - send verification email
GET /customer/<id>/verify - verify a customer account
GET /service/<id>/worker - Get workers providing a service by ID
GET /customer/<id>/booking - Get booking by customer ID
GET /booking/available?customer_id - Get available booking by customer ID
GET /booking/taken?customer_id = Get taken booking by customer ID
GET /customer/<id>/feedback - Get feedback by customer ID
GET /booking/<id>/request - Get requests for a booking by ID
PUT /booking/request/<id>/approve - Approve a request for a booking by request ID
POST /booking - Create booking
  - booking_date (format: DD/MM/YYYY)
  - booking_time (format: HH:MM AM/PM)
  - details
  - service_name
  - address
  - customer_id
  - worker_id (optional)
POST /feedback
  - star
  - feedback_date (optional)
  - details
  - customer_id
  - worker_id
