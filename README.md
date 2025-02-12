# Messenger

This project is a **real-time messaging system** built with **Django** and **Django Rest Framework (DRF)**. It provides an API-based chat system with **WebSocket** support, user authentication via **OTP**, profile management, and real-time message exchange, storing data in **PostgreSQL**.

## Features

### 1. User Authentication
- **Login with a mobile number and OTP** (default code: `12345`)
- If the account does not exist, a **new user account is created**
- **JWT authentication** for secure API access

### 2. Profile Management
- Retrieve user profile information
- Update **username, first name, last name, mobile number, and profile picture**

### 3. Chat Management
- Retrieve a list of chats for the authenticated user
- Fetch a list of **registered users** (with **search by phone number or username**)
- Create a **new chat** with another user
- Get a list of users **previously chatted with**

### 4. Messaging System
- **WebSocket infrastructure** for real-time messaging
- Send and receive **text, images, and files**
- Store all messages in the database

### 5. Additional Features
- **Pagination, search, and sorting** for chat lists and user lists
- **Docker support** with `docker-compose` for easy deployment
- **PostgreSQL** as the main database (can be switched to SQLite if needed)

---

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/hassandn/messenger.git
cd messenger
```

### 2. Run the Project with Docker

#### 1. Create Docker Images
```bash
docker build .
```

#### 2. Create Docker Images with Docker Compose
```bash
docker-compose build
```

#### 3. Run Docker Compose
```bash
docker-compose up -d
```

#### 4. Set Up the Database

##### 1. Make Migrations
```bash
docker-compose exec web python manage.py makemigrations
```

##### 2. Apply Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Additional Information
You can create a superuser or run scripts using this structure:
```bash
docker-compose exec web python manage.py createsuperuser
```

The **Swagger documentation** is complete, but WebSocket integration is not included in it.  
Below is an example URL for using WebSocket in chat:

```url
ws://127.0.0.1:8000/ws/chat/?token=<user-access-token>&chat_id=<chat_id>
```

**Note:** You must have an existing chat between two users, otherwise, you will receive an error.

