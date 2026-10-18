"""Authentication and user management engine."""

from sqlalchemy.orm import Session
from modules.auth.models import User, UserProfile, UserActivity
from modules.auth.schemas import UserLogin, UserRegister, UserProfileUpdate
from modules.auth.security import verify_password
from modules.auth.repository import auth_repository


class AuthEngine:
    @staticmethod
    def register_user(db: Session, data: UserRegister) -> tuple[User | None, str | None]:
        """Register a new user and create their initial user profile."""
        existing = auth_repository.get_by_email(db, data.email)
        if existing:
            return None, "Email is already registered."

        user = auth_repository.create_user(db, data)
        return user, None

    @staticmethod
    def authenticate_user(db: Session, data: UserLogin) -> User | None:
        """Authenticate user credentials and update last login timestamp."""
        user = auth_repository.get_by_email(db, data.email)

        if not user or not verify_password(data.password, user.password_hash):
            return None

        auth_repository.update_last_login(db, user)
        return user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)


    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Fetch user by primary key ID."""
        return auth_repository.get_by_id(db, user_id)

    @staticmethod
    def update_profile(db: Session, user_id: int, data: UserProfileUpdate) -> UserProfile | None:
        """Update or create user profile details."""
        return auth_repository.update_profile(db, user_id, data)

    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> UserProfile | None:
        """Get profile for a specific user ID."""
        return auth_repository.get_profile(db, user_id)

    @staticmethod
    def log_activity(
        db: Session,
        action: str,
        user_id: int | None = None,
        details: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> UserActivity:
        """Create an audit log activity entry."""
        activity = UserActivity(
            user_id=user_id,
            action=action[:80],
            details=details,
            ip_address=ip_address[:64] if ip_address else None,
            user_agent=user_agent,
        )
        db.add(activity)
        db.commit()
        return activity


auth_engine = AuthEngine()
