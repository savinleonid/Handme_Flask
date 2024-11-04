# HandMe - Flask Implementation

### Overview

### Site Screenshots
Below are some screenshots showcasing the interface of HandMe:

![Homepage Screenshot](/app/static/readme/main_page.png)
![Side nav bar](/app/static/readme/loged_in.png)
HandMe is a second-hand product trading web application, implemented in Flask. It replicates the functionality of an earlier Django version of HandMe. Users can register, login, add products, search by filters, edit product information, and delete their accounts or products. The application is styled consistently with the original Django project.

### Features
- User registration, login, logout, and account deletion.
![Login](/app/static/readme/login.png)
![Register](/app/static/readme/register.png)
- Product listing, searching, adding, editing, and deletion.
![Popup delete](/app/static/readme/popup_delete.png)
![Search](/app/static/readme/search.png)
![Edit Product](/app/static/readme/edit_prod_1.png)
- Category filtering and location-based search.
- Profile picture upload.
![Profile](/app/static/readme/profile_1.png)

### Requirements
- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- PostgreSQL

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/savinleonid/HandMe_Flask.git
   cd HandMe_Flask
   ```

2. **Install Dependencies**
   Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**
   Ensure PostgreSQL is installed and running. Update your database configuration in `config.py`.

   Run the migrations to create tables:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Set Up Environment Variables**
   Create a `config.py` file for environment variables like the secret key and database configuration.
   ![config file](/app/static/readme/config.png)

5. **Run the Server**
   ```bash
   flask run
   ```
   Access the application at `http://127.0.0.1:5000/`.

### Project Structure
- **app/**: Main application folder containing all modules and blueprints.
  - **auth/**: Authentication-related logic (register, login, logout).
  - **products/**: Product-related functionality (add, edit, delete).
  - **static/**: CSS, JavaScript, and image files.
  - **templates/**: HTML templates.
- **migrations/**: Database migration files.
- **run.py**: Script to run the Flask server.

### Functionality Notes
- **Product Image Upload**: Users can upload images for their products, which will be saved in the `/static/media/product_images/` directory.
- **CSRF Protection**: The project uses Flask-WTF for CSRF protection, ensuring form security.

### Contributions
Feel free to open issues or create pull requests to improve the project.

### License
This project is open-source and available under the MIT License.

