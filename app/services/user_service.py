"""User Profile and Account management service."""

from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.schemas.user import UserProfileUpdate


class UserService:
    @staticmethod
    def update_profile(db: Session, user_id: int, data: UserProfileUpdate) -> UserProfile | None:
        """Update or create user profile details."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.name = data.name.strip()

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)

        profile.phone = data.phone.strip()
        profile.birth_date = data.birth_date.strip()
        profile.birth_time = data.birth_time.strip()
        profile.birth_city = data.birth_city.strip()
        profile.zodiac_sign = data.zodiac_sign.strip()
        profile.notes = data.notes.strip()

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> UserProfile | None:
        """Get profile for a specific user ID."""
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


user_service = UserService()
