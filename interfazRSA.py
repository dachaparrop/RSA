import tkinter as tk
from tkinter import filedialog

def subir_informacion():
    archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    if archivo:
        status_label.config(text=f"El archivo '{archivo}' se subió correctamente.")
    else:
        status_label.config(text="No se seleccionó ningún archivo.")

def encriptar():
    pass  

def desencriptar():
    pass  

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