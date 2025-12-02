from django.core.management.utils import get_random_secret_key

# Generate a new secret key
secret_key = get_random_secret_key()

# Print the secret key
print(secret_key)
