import ttkbootstrap as ttk  # Importa a biblioteca ttkbootstrap para criar a interface gráfica
from ttkbootstrap.constants import *  # Importa constantes úteis do ttkbootstrap
from PIL import Image, ImageTk  # Importa a biblioteca PIL para trabalhar com imagens
from functools import partial  # Importa partial para facilitar a passagem de argumentos em callbacks
import os  # Importa a biblioteca os para interagir com o sistema operacional
import sys  # Importa a biblioteca sys para acessar variáveis e funções específicas do sistema

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para o PyInstaller """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Caso não esteja usando PyInstaller, usa o caminho atual do diretório
        base_path = os.path.abspath(".")

    # Retorna o caminho completo para o recurso
    return os.path.join(base_path, relative_path)

class Calculadora:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ttk.Window(themename="darkly")  # Cria a janela principal usando ttkbootstrap
        self.janela.geometry('400x750')  # Define o tamanho da janela
        self.janela.title('Calculadora SENAI')  # Define o título da janela
        
        # Definição de cores e fontes
        self.cor_fundo = 'black'  # Cor de fundo da interface
        self.cor_botao = 'secondary'  # Cor dos botões numéricos e de ponto
        self.cor_texto = 'white'  # Cor do texto
        self.cor_operador = 'warning'  # Cor dos botões de operadores
        self.fonte_padrao = ('Roboto', 18)  # Fonte padrão dos botões
        self.fonte_display = ('Roboto', 36)  # Fonte do display

        # Configuração do ícone da janela
        icon_path = resource_path("calc.ico")  # Obtém o caminho do ícone
        self.janela.iconbitmap(icon_path)  # Define o ícone da janela

        # Frame para o display
        self.frame_display = ttk.Frame(self.janela)  # Cria um frame para o display
        self.frame_display.pack(fill='both', expand=True)  # Adiciona o frame ao layout da janela

        # Display para os cálculos
        self.display = ttk.Label(
            self.frame_display, 
            text='', 
            font=self.fonte_display, 
            anchor='e',  # Alinha o texto à direita
            padding=(20, 10)  # Adiciona um preenchimento interno ao rótulo
        )
        self.display.pack(fill='both', expand=True)  # Adiciona o display ao frame

        # Frame para os botões
        self.frame_botoes = ttk.Frame(self.janela)  # Cria um frame para os botões
        self.frame_botoes.pack(fill='both', expand=True)  # Adiciona o frame ao layout da janela

        # Configuração dos botões
        self.botoes = [
            ['C', '⌫', '^', '/'],  # Primeira linha de botões
            ['7', '8', '9', 'x'],  # Segunda linha de botões
            ['4', '5', '6', '+'],  # Terceira linha de botões
            ['1', '2', '3', '-'],  # Quarta linha de botões
            ['.', '0', '()', '=']  # Quinta linha de botões
        ]

        # Criação dos botões
        for i, linha in enumerate(self.botoes):  # Itera sobre as linhas de botões
            for j, texto in enumerate(linha):  # Itera sobre os botões em cada linha
                estilo = 'warning.TButton' if texto in ['C', '⌫', '^', '/', 'x', '+', '-', '='] else 'secondary.TButton'
                botao = ttk.Button(
                    self.frame_botoes,
                    text=texto,
                    style=estilo,
                    width=10,  # Largura do botão
                    command=partial(self.interpretar_botao, texto)  # Define o comando para o botão, usando partial para passar o texto do botão
                )
                botao.grid(row=i, column=j, padx=1, pady=1, sticky='nsew')  # Adiciona o botão ao grid (grade)

        # Configura o redimensionamento das linhas e colunas
        for i in range(5):
            self.frame_botoes.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.frame_botoes.grid_columnconfigure(j, weight=1)

        # Frame para a imagem SENAI
        self.frame_imagem = ttk.Frame(self.janela)  # Cria um frame para a imagem SENAI
        self.frame_imagem.pack(fill='both', expand=True, pady=10)  # Adiciona o frame ao layout da janela

        # Carregando e exibindo a imagem SENAI
        imagem_path = resource_path("Senai.png")  # Obtém o caminho da imagem SENAI
        imagem = Image.open(imagem_path)  # Abre a imagem usando PIL
        imagem = imagem.resize((300, 100), Image.LANCZOS)  # Redimensiona a imagem mantendo a qualidade
        imagem_tk = ImageTk.PhotoImage(imagem)  # Converte a imagem para o formato compatível com tkinter

        label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")  # Cria um rótulo para exibir a imagem
        label_imagem.image = imagem_tk  # Mantém uma referência para a imagem (necessário para evitar que a imagem seja destruída pelo garbage collector)
        label_imagem.pack()  # Adiciona o rótulo ao frame

        # Frame para o seletor de temas
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        # Label "Escolher tema:"
        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        # Seletor de temas (ComboBox)
        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
        self.seletor_tema = ttk.Combobox(self.frame_tema, values=self.temas, state='readonly')
        self.seletor_tema.set('darkly')  # Define o tema padrão
        self.seletor_tema.pack(side='top', fill='x')
        self.seletor_tema.bind('<<ComboboxSelected>>', self.mudar_tema)

        # Inicia a janela principal
        self.janela.mainloop()  # Inicia o loop principal da interface gráfica

    def mudar_tema(self, evento):
        """ Muda o tema da aplicação """
        novo_tema = self.seletor_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        """ Interpreta o botão pressionado e atualiza o display """
        texto_atual = self.display.cget("text")  # Obtém o texto atual do display

        if (valor == 'C'):
            # Limpa o display
            self.display.configure(text='')
        elif (valor == '⌫'):
            # Apaga o último caractere do display
            self.display.configure(text=texto_atual[:-1])
        elif (valor == '='):
            # Calcula o resultado da expressão
            self.calcular()
        elif (valor == '()'):
            # Adiciona parênteses ao display dependendo do contexto
            if not texto_atual or texto_atual[-1] in '+-/^x':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1] in '0123456789)':
                self.display.configure(text=texto_atual + ')')
        else:
            # Adiciona o valor do botão pressionado ao display
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        """ Realiza o cálculo da expressão no display """
        expressao = self.display.cget("text")  # Obtém a expressão do display
        expressao = expressao.replace('x', '*').replace('^', '**')  # Substitui operadores para a sintaxe Python
        
        try:
            # Avalia a expressão e exibe o resultado
            resultado = eval(expressao)
            self.display.configure(text=str(resultado))
        except:
            # Exibe uma mensagem de erro caso a avaliação falhe
            self.display.configure(text="Erro")

# Inicia a aplicação
if __name__ == "__main__":
    Calculadora()  # Instancia a classe Calculadora e inicia o aplicativo