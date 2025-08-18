import customtkinter as ctk
from random import randint
from PIL import Image, ImageTk
import os
import sys

# Função para prevenir erros com imagens ao gerar exe (com Pyinstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Configuração do tema e aparência
ctk.set_appearance_mode("System") # Modos (Light e Dark)
ctk.set_default_color_theme("blue")

# Inicializa a janela principal
root = ctk.CTk()
root.geometry("520x350")
root.title("Gerador de senhas")

# Tenta carregar a imagem (ícone do programa) mas não trava a 
# execusão se não conseguir carregar a imagem
try:
    icon_path = resource_path("senha.ico")
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)
except Exception as e:
    print(f"Não foi possível carregar o ícone: {e}")

# Função para gerar uma nova senha aleatória
def new_rand():
    # Apaga o conteúdo atual (Para garantir que seja gerada uma nova)
    pw_entry.delete(0, ctk.END)

    # Pega a qtd de caracteres que o usuário quer gerar a senha
    pw_length = int(my_entry.get()) if my_entry.get() else 0

    # Gera uma senha usando caracteres da tabela ASCII (carecteres entre 33 e
    # 126 números, letras e símbolos)
    my_password = ''.join(chr(randint(33, 126)) for _ in range(pw_length))

    # Adiciona a senha recém gerada no campo de entrada (pw_entry, começando na
    # posição 0)
    pw_entry.insert(0, my_password)

    # Centraliza a senha no campo
    pw_entry.configure(justify='center')

# Função para copiar a senha gerada

def clipper():
    root.clipboard_clear()
    root.clipboard_append(pw_entry.get())

# Função para limpar os campos de entrada
def clear_entry():
    my_entry.delete(0, ctk.END)
    pw_entry.delete(0, ctk.END)

# Função para validar o comprimento máximo da senha
def validate_length(input):
    if input.isdigit() and len(input) <=2 and int(input) <=32:
        return True
    elif input == "":
        return True
    else:
        return False

#Define a regra de validação para o Entry
validate_command = root.register(validate_length)

# Cria o Frame para o input do comprimento da senha
lf = ctk.CTkFrame(root)
lf.pack(pady=20)

# Label para o input do comprimento da senha
ctk.CTkLabel(lf, text="Quantos caracteres (Máximo 32)?",font=("Helvetica", 16)).pack(pady=10)

# Input para senha (Aplicando a validação)
# Obs: '%P' (Parâmetro especial que passa o texto para a função)

my_entry = ctk.CTkEntry(lf, font=("Helvetica", 24), validate="key", validatecommand=(validate_command, '%P'), width=80, justify='center')
my_entry.pack(pady=10)

# Input para exibir a senha gerada
pw_entry = ctk.CTkEntry(root, font=("Helvetica", 24),justify='center', width=500)
pw_entry.pack(pady=20)

# Frame para organizar os botões
my_frame = ctk.CTkFrame(root)
my_frame.pack(pady=20)

# Carrega as imagens para os botões
try:
    create_image = ctk.CTkImage(light_image=Image.open(resource_path("create.png")),dark_image=Image.open(resource_path("create.png")), size=(20,20))
    create_image = ctk.CTkImage(light_image=Image.open(resource_path("copy.png")),dark_image=Image.open(resource_path("copy.png")), size=(20,20))
    create_image = ctk.CTkImage(light_image=Image.open(resource_path("clean.png")),dark_image=Image.open(resource_path("clean.png")), size=(20,20))
except Exception as e:
    print(f"Não foi possível carregar uma ou mais imagens dos botões: {e}")
    create_image = copy_image = clean_image =None

# Botão para gerar senha forte (verde)
my_button = ctk.CTkButton(my_frame, text="Gerar senha forte", command=new_rand, image=create_image, compound="left", font=("Helvetica", 16), fg_color="#4CAF50", hover_color="#45a049")
my_button.grid(row=0, column=0, padx=10)

# Botão para copiar
clip_button = ctk.CTkButton(my_frame, text="Copiar", command=clipper, image=create_image, compound="left", font=("Helvetica", 16))
clip_button.grid(row=0, column=1, padx=10)

# Botão para limpar os campos (laranja)
clear_button = ctk.CTkButton(my_frame, text="Limpar", command=clear_entry, image=create_image, compound="left", font=("Helvetica", 16), fg_color="#ff8000", hover_color="#F57c00")
clear_button.grid(row=0, column=2, padx=10)


# Exibe a tela principal
root.mainloop()