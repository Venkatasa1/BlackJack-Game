# BlackJack Game

## Project Description
This project is a web application designed to handle user authentication and gameplay features. It includes multiple HTML templates for different user interactions such as login, signup, viewing scores, and more.

## Project Structure
- `application.py`: The main application script that runs the web server.
- `config.py`: Configuration file containing environment variables and settings.
- `database.sql`: SQL script for setting up the project's database.
- `Templates/`: A directory that contains the following HTML templates:
  - `Index.html`: The homepage or landing page.
  - `Login.html`: The user login page.
  - `Signup.html`: The user registration page.
  - `gameplay.html`: A page dedicated to the core gameplay feature.
  - `View_Scores.html`: A page for users to view their scores.
  - `Welcome_note.html`: A welcome message or dashboard displayed after login.

## Dependencies
This project requires the following dependencies:
- Python 3.x
- Flask (or another relevant web framework)
- A SQL-based database

These dependencies can be installed using:

```bash
pip install -r requirements.txt
```

## Setup Instructions
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/your-repository-name.git
    ```
2. Navigate to the project directory:
    ```bash
    cd BlackJack_Game
    ```
3. Set up the database:
    ```bash
    # If using MySQL
    mysql -u your-username -p your-database-name < database.sql
    ```
4. Run the application:
    ```bash
    python application.py
    ```

## Usage
- Open your web browser and go to `http://localhost:5000` (or the appropriate port).
- Interact with the application by creating an account, logging in, and engaging with the gameplay features.

