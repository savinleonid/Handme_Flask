from flask import render_template, request, current_app
from flask_login import login_required, current_user
from app import db
from . import prof_bp

from werkzeug.utils import secure_filename
import os


@prof_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file:
            filename = secure_filename(file.filename)
            profile_dir = os.path.join(current_app.static_folder, 'media/profile_pics')

            # Ensure the profile_pics directory exists
            if not os.path.exists(profile_dir):
                os.makedirs(profile_dir)

            file_path = os.path.join(profile_dir, filename)
            file.save(file_path)

            # Update the user's profile picture path in the database
            current_user.profile.profile_picture = f'media/profile_pics/{filename}'
            db.session.commit()

    return render_template('app/profile.html')  # Update to use the correct template

