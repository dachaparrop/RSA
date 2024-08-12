import tkinter as tk
import os

from tkinter import filedialog, messagebox
from RSA import *


def keys_exist():
    """
        Check if the RSA key files (public and private) already exist in the 'keys' directory.
    """

    if not os.path.exists("keys"):
        os.makedirs("keys")

    public_key_path = os.path.join("keys", "public_key.txt")
    private_key_path = os.path.join("keys", "private_key.txt")

    return os.path.exists(public_key_path) and os.path.exists(private_key_path)


def generate_keys():
    """
        Generate a new RSA key pair and save them as 'public_key.txt' and 'private_key.txt' in the 'keys' directory.
    """
    
    try: 
        bits = 1024
        p, q = generate_large_primes(bits)
        public_key, private_key = generate_keypair(p, q)

        if not os.path.exists("keys"):
            os.makedirs("keys")
        
        public_key_path = os.path.join("keys", "public_key.txt")
        with open(public_key_path, 'w') as file:
            file.write(f"{public_key[0]}\n{public_key[1]}")

        private_key_path = os.path.join("keys", "private_key.txt")
        with open(private_key_path, 'w') as file:
            file.write(f"{private_key[0]}\n{private_key[1]}")

        messagebox.showinfo("Keys Generated", "New keys have been generated.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def get_public_key():
    """
        Retrieve the public key from the 'public_key.txt' file in the 'keys' directory.
    """

    try:
        public_key_path = os.path.join("keys", "public_key.txt")

        with open(public_key_path, 'r') as file:
            e = int(file.readline().strip())
            n = int(file.readline().strip())
            public_key = (e, n)
        return public_key
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the public key: {str(e)}")
        return None


def get_private_key():
    """
        Retrieve the private key from the 'private_key.txt' file in the 'keys' directory.
    """
    
    try:
        private_key_path = os.path.join("keys", "private_key.txt")

        with open(private_key_path, 'r') as file:
            d = int(file.readline().strip())
            n = int(file.readline().strip())
            private_key = (d, n)
        return private_key
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the private key: {str(e)}")
        return None 


def upload_file():
    """
        Opens a file dialog for the user to select a file to upload.
    """
    
    file = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt")]  
    )
    if file:
        status_label.config(text=f"The file '{file}' was uploaded successfully.")
        root.filename = file  
    else:
        status_label.config(text="No file was selected.")


def encrypt_file():
    """
        Encrypt the contents of the selected file using the public key.
        If keys don't exist, it generates new keys.
        The encrypted content is then saved to a new file chosen by the user.
    """

    try:
        if not hasattr(root, 'filename'):
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        with open(root.filename, 'r') as file:
            content = file.read()

        if not keys_exist():
            generate_keys()

        public_key = get_public_key()
        encrypted_content = encrypt(public_key, content)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Encrypted File")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(' '.join(map(str, encrypted_content)))
            status_label.config(text=f"The file has been encrypted and saved as '{save_path}'.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def decrypt_file():
    """
        Decrypt the contents of the selected encrypted file using the private key.
        The decrypted content is then saved to a new file chosen by the user.
    """
    
    try:
        if not hasattr(root, 'filename'):
            messagebox.showwarning("Warning", "Please select a file first.")
            return

        with open(root.filename, 'r') as file:
            encrypted_content = file.read()

        encrypted_content = list(map(int, encrypted_content.split()))

        if not keys_exist():
            messagebox.showwarning("Warning", "Please select a private key file first.")
            return

        private_key = get_private_key()
        decrypted_content = decrypt(private_key, encrypted_content)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Decrypted File")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(decrypted_content)
            status_label.config(text=f"The file has been decrypted and saved as '{save_path}'.")

    except ValueError as ve:
        messagebox.showerror("Error", "Conversion error: Please ensure the file contains correctly encrypted data.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def change_keys():
    """
        Generate new RSA keys, replacing the existing ones.
        If keys already exist, it prompts the user for confirmation before generating new keys.
    """

    try:
        if keys_exist():
            response = messagebox.askyesno(
                "Confirm", 
                "Keys already exist. If you generate new ones, the old ones will be lost. Do you want to continue?"
            )
            if not response:
                return

        generate_keys()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while trying to change the keys: {str(e)}")


root = tk.Tk()
root.title("Encryption Interface")
root.geometry("500x400")
root.configure(bg="#e6e6e6")  
root.resizable(False, False)

button_style = {
    "bg": "#80c1ff", 
    "fg": "black",  
    "font": ("Helvetica", 12, "bold"),
    "padx": 10,
    "pady": 5
}

upload_btn = tk.Button(root, text="UPLOAD FILE", command=upload_file, **button_style)
upload_btn.place(x=50, y=30)

status_label = tk.Label(root, bg="#e6e6e6", font=("Helvetica", 10), wraplength=200, anchor="w")
status_label.place(x=280, y=30)

encrypt_btn = tk.Button(root, text="ENCRYPT", command=encrypt_file, **button_style)
encrypt_btn.place(x=150, y=100)

decrypt_btn = tk.Button(root, text="DECRYPT", command=decrypt_file, **button_style)
decrypt_btn.place(x=280, y=100)

change_keys_btn = tk.Button(root, text="CHANGE KEYS\n(PUBLIC/PRIVATE)", command=change_keys, **button_style)
change_keys_btn.place(x=150, y=180)

key_label = tk.Label(root, text="Graphical representation of the private key (optional)\n(For the user to know if their key has changed)", bg="#e6e6e6", font=("Helvetica", 10))
key_label.place(x=100, y=260)

decrypted_info_label = tk.Label(root, text="(Displays the decrypted information)", bg="#e6e6e6", font=("Helvetica", 10))
decrypted_info_label.place(x=150, y=330)


root.mainloop()
