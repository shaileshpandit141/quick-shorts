# Django, React and TypeScript Boilerplate with JWT Authentication

This project is a boilerplate for setting up a web application using Django for the backend with JWT (JSON Web Token) authentication, and React with TypeScript for the frontend.

## Features

- Django backend with custom user model (using email authentication)
- JWT Authentication for all actions 
- React with TypeScript frontend setup with Create React App
- Integration between Django and React

## Requirements

- Python 3.8+
- Node.js 14+
- npm (or yarn)
- PostgreSQL (default: db.sqlite3)

## Setup Instructions

### Backend Setup (Django)

1. **Clone the repository:**

  ```bash
  git clone https://github.com/yourusername/your-repo-name.git
  cd your-repo-name
  ```

2. **Create a virtual environment:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies:**

  ```bash
  pip install -r requirements.txt
  ```

4. **Set up environment variables:**

  Create a `.env` file in the root directory and add the following:

  ```plaintext
  HOST=localhost
  PORT=8000
  SEND_VERIFICATION_URL_HOST=localhost
  SEND_VERIFICATION_URL_PORT=3000
  SECRET_KEY=your_secret_key
  DEBUG=True
  ALLOWED_HOSTS=localhost,
  CORS_ALLOWED_ORIGINS=http://localhost:3000,

  # Uncomment and configure the following for PostgreSQL:
  # DB_NAME=your_db_name
  # DB_USER=your_db_user
  # DB_PASSWORD=your_db_password
  # DB_HOST=localhost
  # DB_PORT=5432

  # Email Configuration
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_USE_SSL=False
  EMAIL_HOST_USER=your_email@example.com
  EMAIL_HOST_PASSWORD=your_email_password
  DEFAULT_FROM_EMAIL=your_email@example.com
  ```

5. **Apply migrations:**

  ```bash
  python manage.py migrate
  ```

6. **Create a superuser:**

  ```bash
  python manage.py createsuperuser
  ```

7. **Run the development server:**

  ```bash
  python manage.py runserver
  ```

### Frontend Setup (React with TypeScript)

1. **Navigate to the frontend directory:**

  ```bash
  cd frontend
  ```

2. **Create new TypeScript React app:**

  ```bash
  npx create-react-app . --template typescript
  ```

3. **Install dependencies:**

  ```bash
  npm install
  ```

4. **Set up environment variables:**

  Create a `.env` file in the root directory and add the following:

  ```plaintext
  HOST=localhost
  PORT=3000
  REACT_APP_BASE_API_URL=http://localhost:8000/
  ```
  Note: `HOST` name is same as backend `HOST` name.

5. **Run the React development server:**

  ```bash
  npm start
  ```

### Configuration


### Performing Authentication Actions API's

- **Registration**:
Send a POST request to `http://localhost:8000/api/v1/auth/signup/` with user details (email, password1, password2).

- **Login**:
Send a POST request to `http://localhost:8000/api/v1/auth/token/` with email and password to get access and refresh tokens.

- **Logout**:
Send a POST request to `http://localhost:8000/api/v1/auth/signout/` to log out the user and blacklist the refresh token.

- **Password Reset**:
Send a POST request to `http://localhost:8000/api/v1/auth/password/reset/` with the user's email.

- **Password Reset Verification**:
Send a POST request to `http://localhost:8000/api/v1/auth/password/reset/confirm/` with the new password and token received from the email.

- **Email Verification**:
Send a POST request to `http://localhost:8000/api/v1/auth/signup/verify-email/` with the verification key received in the email.

- **Re Email Verification**:
Send a POST request to `http://localhost:8000/api/v1/auth/signup/resend-email-verification/` with email to get key received in the email.

- **Token Refresh**:
Send a POST request to `http://localhost:8000/api/v1/auth/token/refresh/` with the refresh token to get a new access token.

- **Access the user**:
Send a POST request to `http://localhost:8000/api/v1/auth/user/` with the access token to get a userInfo.

- **Access a protected endpoint for test**:
Send a POST request to `http://localhost:8000/api/v1/auth/protected/` with the access token to get a protected route data.


### API's Usages using .rest file

**Register a new user:**
```
POST http://localhost:8000/api/v1/auth/signup/
Content-Type: application/json

{
  "email": "email@example.com",
  "password1": "Email#12345@",
  "password2": "Email#12345@"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "Verification e-mail sent."
  },
  "meta": null
}
```

Error response:
```
{
  "status": "error", 
  "message": "The request was not successful",
  "error": {
    "email": "Invalid email address",
    "password1": "Invalid password1",
    "password2": "Invalid password2"
  }
}
```

**Login to get JWT tokens:**
```
POST http://localhost:8000/api/v1/auth/token/
Content-Type: application/json

{
  "email": "email@example.com",
  "password": "Email#12345@"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "access_token": "jwt_access_token",
    "refresh_token": "jwt_refresh_token"
  },
  "meta": null
}
```

Error response:
```
{
  "status": "error",
  "message": "The request was not successful", 
  "error": {
    "detail": "No active account found with the given credentials"
  }
}
```

**Logout (Blacklist the refresh token):**
```
POST http://localhost:8000/api/v1/auth/logout/
Content-Type: application/json
Authorization: Bearer jwt_access_token

{
  "refresh_token": "jwt_refresh_token"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "You have signed out successfully."
  },
  "meta": null
}
```

**Request password reset:**
```
POST http://localhost:8000/api/v1/auth/password/reset/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "Password reset e-mail has been sent."
  },
  "meta": null
}
```

**Confirm password reset:**
```
POST http://localhost:8000/api/v1/auth/password/reset/confirm/
Content-Type: application/json

{
  "uid": "uid_from_email",
  "token": "token_from_email",
  "new_password1": "new_strong_password123",
  "new_password2": "new_strong_password123"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "Password has been reset with the new password."
  },
  "meta": null
}
```

**Verify email:**
```
POST http://localhost:8000/api/v1/auth/signup/verify-email/
Content-Type: application/json

{
  "key": "verification_key_from_email"
}
```

Success response:
```
{
  "status": "success", 
  "message": "The request was successful",
  "data": {
    "detail": "ok"
  },
  "meta": null
}
```

**Resend Verification Email:**
```
POST http://localhost:8000/api/v1/auth/signup/resend-email-verification/
Authorization: Bearer <your_jwt_token>
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "Verification e-mail sent"
  },
  "meta": null
}
```

**Refresh JWT tokens:**
```
POST http://localhost:8000/api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh_token": "jwt_refresh_token"
}
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "access_token": "new_jwt_access_token"
  },
  "meta": null
}
```

**Access the current user:**
```
GET http://localhost:8000/api/v1/auth/user/
Authorization: Bearer jwt_access_token
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "id": 1,
    "email": "email@example.com",
    "first_name": "first_name",
    "last_name": "last_name"
  },
  "meta": null
}
```

**Access a protected endpoint:**
```
GET http://localhost:8000/api/v1/auth/protected/
Authorization: Bearer jwt_access_token
```

Success response:
```
{
  "status": "success",
  "message": "The request was successful",
  "data": {
    "detail": "This is a protected view"
  },
  "meta": null
}
```

**Frontend:**

The React frontend should handle authentication by storing the JWT tokens in localStorage or a similar mechanism and including the access token in the Authorization header for protected requests. TypeScript interfaces should be used for type checking of API responses and request payloads.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Author
If you have any questions or need assistance with this project, please contact `Shailesh` at `shaileshpandit141@gmail.com`.

Thank you
