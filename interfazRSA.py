import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from RSA import *

def subir_informacion():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Text files", "*.txt")]  
    )
    if archivo:
        status_label.config(text=f"El archivo '{archivo}' se subió correctamente.")
        root.filename = archivo  
    else:
        status_label.config(text="No se seleccionó ningún archivo.")

def encriptar():
    try:
        if not hasattr(root, 'filename'):
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo primero.")
            return

        with open(root.filename, 'r') as file:
            content = file.read()

        bits = 1024
        p, q = generate_large_primes(bits)
        public_key, private_key = generate_keypair(p, q)

        encrypted_content = encrypt(public_key, content)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar archivo encriptado")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(' '.join(map(str, encrypted_content)))
            status_label.config(text=f"El archivo ha sido encriptado y guardado como '{save_path}'.")

            private_key_path = save_path.replace(".txt", "_private_key.txt")
            with open(private_key_path, 'w') as file:
                file.write(f"{private_key[0]}\n{private_key[1]}")
            messagebox.showinfo("Llave privada guardada", f"La llave privada se ha guardado en '{private_key_path}'.")

    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")


def desencriptar():
    try:
        if not hasattr(root, 'filename'):
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo primero.")
            return

        with open(root.filename, 'r') as file:
            encrypted_content = file.read()

        encrypted_content = list(map(int, encrypted_content.split()))

        private_key_file = filedialog.askopenfilename(title="Selecciona el archivo de la llave privada")
        if not private_key_file:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de llave privada primero.")
            return

        with open(private_key_file, 'r') as file:
            private_key = tuple(map(int, file.read().splitlines()))

        decrypted_content = decrypt(private_key, encrypted_content)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Guardar archivo desencriptado")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(decrypted_content)
            status_label.config(text=f"El archivo ha sido desencriptado y guardado como '{save_path}'.")

    except ValueError as ve:
        messagebox.showerror("Error", "Error de conversión: Verifica que el archivo contenga datos cifrados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")

def cambiar_llaves():
    pass


root = tk.Tk()
root.title("Interfaz de Encriptación")
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

subir_btn = tk.Button(root, text="SUBIR INFORMACIÓN", command=subir_informacion, **button_style)
subir_btn.place(x=50, y=30)

status_label = tk.Label(root, bg="#e6e6e6", font=("Helvetica", 10), wraplength=200, anchor="w")
status_label.place(x=280, y=30)

encriptar_btn = tk.Button(root, text="ENCRIPTAR", command=encriptar, **button_style)
encriptar_btn.place(x=150, y=100)

desencriptar_btn = tk.Button(root, text="DESENCRIPTAR", command=desencriptar, **button_style)
desencriptar_btn.place(x=280, y=100)

cambiar_llaves_btn = tk.Button(root, text="CAMBIAR LLAVES\n(PÚBLICA/PRIVADA)", command=cambiar_llaves, **button_style)
cambiar_llaves_btn.place(x=150, y=180)

llave_label = tk.Label(root, text="Figura gráfica de la llave privada (opcional)\n(Es para que el usuario sepa si su llave cambió)", bg="#e6e6e6", font=("Helvetica", 10))
llave_label.place(x=100, y=260)


info_desencriptada_label = tk.Label(root, text="(Muestra la información desencriptada)", bg="#e6e6e6", font=("Helvetica", 10))
info_desencriptada_label.place(x=150, y=330)


root.mainloop()