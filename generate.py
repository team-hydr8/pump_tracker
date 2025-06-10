import bcrypt
import sys

def hash_new_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <password_to_hash>")
        sys.exit(1)

    plain_text_password = sys.argv[1]
    hashed_password = hash_new_password(plain_text_password)

    print(f"\nPlain Text: {plain_text_password}")
    print(f"Hashed Value: {hashed_password}")