from research_agent.security.auth import hash_password, verify_pasword

password = "mypassword123"

hashed = hash_password(password)

print("Original:", password)
print("Hashed:", hashed)

print("Correct password:",
      verify_pasword(password, hashed))

print("Wrong password:",
      verify_pasword("wrongpassword", hashed))