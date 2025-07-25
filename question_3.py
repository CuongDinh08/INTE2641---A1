# Student ID: S4032825
# Student name: Dinh Ngoc Hoang Cuong

# I got the idea to use the `cryptography` library to generate a key pair
# from: https://stackoverflow.com/questions/2466401/how-to-generate-ssh-key-pairs-with-python
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os
from termcolor import colored


def clear_console() -> None:
    """
    This function clears the console.
    Source: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    clear_console()  # Clear the console for a fresh start

    # -------------- Task 1 --------------

    # Generate the full key
    raw_key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)
    input("Successfully generated a key pair! Press Enter to see the private key...")
    
    # Separate the private and public keys
    private_key = raw_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = raw_key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    # Show the generated keys
    clear_console()  # Clear the console for a fresh start
    print(colored("------- Bellow is the private key, DO NOT SHARE IT! -------", "red"), end="\n\n")
    print(private_key.decode(), end="\n\n")
    input("Press Enter to see the public key...")

    clear_console()  # Clear the console for a fresh start
    print(colored("------- Bellow is the public key, you could share it to anyone. -------", "green"), end="\n\n")
    title = colored("Public key:", "blue")
    print(f"{ title } {public_key.decode()}", end="\n\n")
    input("Press Enter to move on to the next step...")

    # -------------- Task 2 --------------

    # Enter a message to encrypt
    clear_console()  # Clear the console for a fresh start
    message = input(colored("Enter a message to encrypt: ", "blue"))

    # -------------- Task 3 --------------

    # Sign the message with the private key
    clear_console()  # Clear the console for a fresh start
    signature = raw_key.sign(
        message.encode(),
        # Padding is used to ensure the signature is secure
        # and make the structure of the signature unpredictable
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), # MGF1 is a mask generation function 
            salt_length=padding.PSS.MAX_LENGTH # Maximum length of salt
        ),
        hashes.SHA256() # SHA256 is a cryptographic hash function. In this case, it is used to hash the message before signing
    )
    title = colored("This is the message signed by the private key:", "blue")
    print(f"{ title } { signature.hex() }", end="\n\n")
    input("Press Enter to verify the signature...")

    # -------------- Task 4 --------------

    clear_console()  # Clear the console for a fresh start
    # Verify the signature with the public key
    title = colored("Verification status:", "blue")
    # The defailt status is invalid
    status = colored("Invalid!", "red")
    try:
        raw_key.public_key().verify(
            signature, message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        status = colored("Valid!", "green")
    except Exception as exc:
        ...
    finally:
        print(f"{ title } { status }", end="\n\n")
        input("Press Enter to verify the signature with another key...")

    # -------------- JUST FOR FUN =)) --------------

    clear_console()  # Clear the console for a fresh start
    another_raw_key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)
    title = colored("Generated another key with the private key:", "blue")
    print(title, end="\n\n")
    print(another_raw_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode(), end="\n\n")
    
    # Verify the signature with the another public key
    title = colored("Verification status with another key:", "blue")
    status = colored("Invalid!", "red")
    try:
        another_raw_key.public_key().verify(
            signature, message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        status = colored("Valid!", "green")
    except Exception as exc:
        ...
    finally:
        print(f"{ title } { status }", end="\n\n")
        input("Press Enter to encrypt the message with the old public key...")

    
    # Encrypt the message with the public key
    clear_console()  # Clear the console for a fresh start
    ciphertext = raw_key.public_key().encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    title = colored("Encrypted message with the public key:", "blue")
    print(f"{ title } {ciphertext.hex()}", end="\n\n")
    input("Press Enter to decrypt the message with the private key...")

    clear_console()

    # Decrypt the message with the private key
    decrypted_message = raw_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    title = colored("Decrypted message with the private key:", "blue")
    print(f"{ title } {decrypted_message.decode()}")
