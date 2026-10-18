from datetime import datetime
from sqlalchemy.orm import Session
from modules.auth.models import User, UserProfile, AdminUser, UserActivity
from modules.auth.schemas import UserRegister, UserProfileUpdate
from modules.auth.security import hash_password


class AuthRepository:
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.strip().lower()).first()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, data: UserRegister) -> User:
        user = User(
            name=data.name.strip(),
            email=data.email.strip().lower(),
            password_hash=hash_password(data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        profile = UserProfile(
            user_id=user.id,
            phone=data.phone.strip() if data.phone else None,
        )
        db.add(profile)
        db.commit()
        return user

    def update_last_login(self, db: Session, user: User) -> None:
        user.last_login_at = datetime.utcnow()
        db.commit()

    def get_profile(self, db: Session, user_id: int) -> UserProfile | None:
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def update_profile(self, db: Session, user_id: int, data: UserProfileUpdate) -> UserProfile | None:
        user = self.get_by_id(db, user_id)
        if not user:
            return None

        user.name = data.name.strip()

        profile = self.get_profile(db, user_id)
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


auth_repository = AuthRepository()
