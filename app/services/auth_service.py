"""Authentication, registration, and session management service."""

from datetime import datetime
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User, UserProfile
from app.schemas.auth import UserLogin, UserRegister


class AuthService:
    @staticmethod
    def register_user(db: Session, data: UserRegister) -> tuple[User | None, str | None]:
        """Register a new user and create their initial user profile."""
        email = data.email.strip().lower()

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return None, "Email is already registered."

        user = User(
            name=data.name.strip(),
            email=email,
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

        return user, None

    @staticmethod
    def authenticate_user(db: Session, data: UserLogin) -> User | None:
        """Authenticate user credentials and update last login timestamp."""
        email = data.email.strip().lower()
        user = db.query(User).filter(User.email == email).first()

        if not user or not verify_password(data.password, user.password_hash):
            return None

        user.last_login_at = datetime.utcnow()
        db.commit()
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Fetch user by primary key ID."""
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()


auth_service = AuthService()
