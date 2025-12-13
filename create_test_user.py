#!/usr/bin/env python3
"""
Script to create a test user in the database for development/testing purposes.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database.database import SessionLocal, engine, Base
from backend.database.models import User
from backend.utils.password_hashing import hash_password

def create_test_user():
    """Create a test user with ID=1 for development."""

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if user with ID=1 already exists
        existing_user = db.query(User).filter(User.id == 1).first()

        if existing_user:
            print(f"✓ Test user already exists: {existing_user.username} (ID: {existing_user.id})")
            return

        # Create test user
        test_user = User(
            username="testuser",
            password_hash=hash_password("password123")
        )

        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        print(f"✓ Test user created successfully!")
        print(f"  Username: {test_user.username}")
        print(f"  Password: password123")
        print(f"  User ID: {test_user.id}")

    except Exception as e:
        print(f"✗ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
