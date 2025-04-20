from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with ratings
    ratings = db.relationship('Rating', backref='teacher', lazy='dynamic', cascade="all, delete-orphan")
    
    @property
    def avg_rating(self):
        """Calculate the average rating for this teacher"""
        result = db.session.query(func.avg(Rating.score)).filter(Rating.teacher_id == self.id).scalar()
        return round(result, 1) if result is not None else 0
    
    @property
    def rating_count(self):
        """Get the number of ratings for this teacher"""
        return Rating.query.filter_by(teacher_id=self.id).count()
    
    @property
    def rating_distribution(self):
        """Get distribution of ratings (count for each score 1-5)"""
        distribution = {}
        for i in range(1, 6):
            distribution[i] = Rating.query.filter_by(teacher_id=self.id, score=i).count()
        return distribution

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)  # Score from 1-5
    comment = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)  # Support for IPv6
    
    # Foreign key to teacher
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    
    __table_args__ = (
        # Create a unique constraint on teacher_id and ip_address
        # to prevent multiple ratings from the same IP
        db.UniqueConstraint('teacher_id', 'ip_address', name='unique_teacher_ip'),
    )
