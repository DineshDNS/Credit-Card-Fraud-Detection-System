from app.core.security import verify_password

hashed = "$2b$12$DZynGJwzbllR6wGsNV/LKuvy7IbvEY0mYTIRDtlIE1z/2wxuE3qjK"

print(
    verify_password(
        "admin123",
        hashed
    )
)