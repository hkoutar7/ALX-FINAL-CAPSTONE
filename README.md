# Blog API Plateform : BlogPuilsem

## Description

An MVP API Project for managing blog posts and user profiles. Features include post management, search, and user authentication.

## Features

- Post CRUD operations
- Category, author, and search filters
- User authentication and profile management

## Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- Swagger UI


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourproject.git
    ```

2. Set up the virtual environment:

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the server:

    ```bash
    python manage.py runserver
    ```

## API Documentation

Access Swagger UI: `http://127.0.0.1:8000/docs/`

## API Endpoints

### Auth Managment
- **POST** `/api/v1/login`: Login
- **POST** `/api/v1/register`: Register
- **GET** `/api/v1/me`: User profile

### Users Managment
- **GET** `/api/v1/users`: List all users
- **GET** `/api/v1/users/{id}`: Get a user
- **UPDATE** `/api/v1/users/{id}`: update a user
- **DELETE** `/api/v1/users/{id}`: delete a user



### Posts
- **GET** `/api/v1/posts`: List posts (ALL)
- **GET** `/api/v2/posts`: List posts (WITH PAGINATION - CHUNKS OF DATA)
- **POST** `/api/v1/posts`: Create a post
- **GET** `/api/v1/posts/{id}`: Get a post
- **PUT** `/api/v1/posts/{id}`: Update a post
- **DELETE** `/api/v1/posts/{id}`: Delete a post
- **GET** `/api/v1/posts/category/{category_id}`: Get Posts by category
- **GET** `/api/v1/posts/author/{author_id}`: Get Posts by author
- **GET** `/api/v1/posts/search`: Search posts by title, content, author, tags


## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your branch to your fork.
5. Submit a pull request to the main repository.
## Authors

- [hkoutar7](https://github.com/hkoutar7)

## License

MIT License
