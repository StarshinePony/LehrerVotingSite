import logging
from flask import render_template, redirect, url_for, flash, request, abort, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app import app, db
from models import Admin, Teacher, Rating
from forms import LoginForm, TeacherForm, RatingForm

# Helper function to get client IP address
def get_client_ip():
    """
    Get the client's IP address from the request.
    This handles both direct client connections and proxy forwarding.
    """
    if request.headers.get('X-Forwarded-For'):
        # Using first forwarded IP if provided
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        return request.remote_addr

# User-facing routes
@app.route('/')
def index():
    teachers = Teacher.query.all()
    return render_template('index.html', teachers=teachers)

@app.route('/teacher/<int:teacher_id>', methods=['GET', 'POST'])
def teacher_detail(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = RatingForm()
    
    # Check if the client IP has already voted for this teacher
    client_ip = get_client_ip()
    existing_rating = Rating.query.filter_by(teacher_id=teacher_id, ip_address=client_ip).first()
    has_rated = existing_rating is not None
    
    if form.validate_on_submit():
        if has_rated:
            flash('Sie haben diesen Lehrer bereits bewertet.', 'warning')
            return redirect(url_for('teacher_detail', teacher_id=teacher_id))
            
        try:
            rating = Rating(
                score=form.score.data,
                comment=form.comment.data,
                teacher_id=teacher_id,
                ip_address=client_ip
            )
            db.session.add(rating)
            db.session.commit()
            flash('Ihre Bewertung wurde übermittelt. Vielen Dank!', 'success')
            return redirect(url_for('teacher_detail', teacher_id=teacher_id))
        except IntegrityError:
            db.session.rollback()
            flash('Sie haben diesen Lehrer bereits bewertet.', 'warning')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error submitting rating: {e}")
            flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.', 'danger')
    
    # Get all ratings for this teacher
    ratings = Rating.query.filter_by(teacher_id=teacher_id).order_by(Rating.timestamp.desc()).all()
    
    return render_template('teacher_detail.html', 
                          teacher=teacher, 
                          form=form, 
                          ratings=ratings,
                          has_rated=has_rated)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If already logged in, redirect to admin dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            flash('Anmeldung erfolgreich!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        flash('Ungültiger Benutzername oder Passwort', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Sie wurden abgemeldet.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    teachers = Teacher.query.all()
    return render_template('admin/dashboard.html', teachers=teachers)

@app.route('/admin/teacher/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            name=form.name.data,
            subject=form.subject.data,
            bio=form.bio.data
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Lehrer erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_teacher.html', form=form, title="Lehrer hinzufügen")

@app.route('/admin/teacher/edit/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = TeacherForm(obj=teacher)
    
    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.subject = form.subject.data
        teacher.bio = form.bio.data
        db.session.commit()
        flash('Lehrer erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/add_teacher.html', form=form, title="Lehrer bearbeiten")

@app.route('/admin/teacher/delete/<int:teacher_id>', methods=['POST'])
@login_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Lehrer erfolgreich gelöscht!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/rating/delete/<int:rating_id>', methods=['POST'])
@login_required
def delete_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    teacher_id = rating.teacher_id
    db.session.delete(rating)
    db.session.commit()
    flash('Kommentar erfolgreich gelöscht!', 'success')
    return redirect(url_for('teacher_detail', teacher_id=teacher_id))

@app.route('/api/teacher/<int:teacher_id>/ratings')
def teacher_ratings_data(teacher_id):
    """Return the rating distribution data for a teacher in JSON format for Chart.js"""
    teacher = Teacher.query.get_or_404(teacher_id)
    distribution = teacher.rating_distribution
    
    data = {
        'labels': ['1 Stern', '2 Sterne', '3 Sterne', '4 Sterne', '5 Sterne'],
        'values': [distribution[1], distribution[2], distribution[3], distribution[4], distribution[5]]
    }
    
    return jsonify(data)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Seite nicht gefunden"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Interner Serverfehler"), 500
