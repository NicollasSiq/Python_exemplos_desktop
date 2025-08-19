import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

# BANCO DE DADOS
conn = sqlite3.connect("despesas.db")  # Conecta/cria o banco de dados SQLite
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL
    )
""")  # Cria a tabela de transações se não existir
conn.commit()

# APP
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Despesas")  # Título da janela
        self.geometry("600x400")  # Tamanho da janela

        # Formulário de entrada de dados
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=10, pady=10)

        self.tipo = ctk.StringVar(value="Despesa")  # Tipo da transação (Receita/Despesa)
        ctk.CTkOptionMenu(frame, values=["Receita", "Despesa"], variable=self.tipo).grid(row=0, column=0, padx=5, pady=5)

        self.ent_desc = ctk.CTkEntry(frame, placeholder_text="Descrição")  # Campo descrição
        self.ent_desc.grid(row=0, column=1, padx=5, pady=5)

        self.ent_valor = ctk.CTkEntry(frame, placeholder_text="Valor (ex: 100.50)")  # Campo valor
        self.ent_valor.grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkButton(frame, text="Adicionar", command=self.add_transacao).grid(row=0, column=3, padx=5, pady=5)  # Botão adicionar

        # Exibe o saldo atual
        self.lbl_saldo = ctk.CTkLabel(self, text="Saldo: R$ 0.00", font=("Arial", 16, "bold"))
        self.lbl_saldo.pack(pady=5)

        # Tabela para listar as transações
        cols = ("id", "tipo", "descricao", "valor", "data")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column("id", width=40)
        self.tree.column("valor", width=80, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botão para excluir transação selecionada
        ctk.CTkButton(self, text="Excluir Selecionado", fg_color="red", command=self.del_transacao).pack(pady=5)

        self.carregar()  # Carrega os dados iniciais

    # Função para adicionar uma nova transação
    def add_transacao(self):
        tipo = self.tipo.get()
        desc = self.ent_desc.get().strip()
        try:
            valor = float(self.ent_valor.get().replace(",", "."))
        except:
            messagebox.showerror("Erro", "Valor inválido!")
            return
        data = datetime.now().strftime("%d/%m/%Y")

        if not desc:
            messagebox.showwarning("Aviso", "Descrição obrigatória!")
            return

        # Insere a transação no banco de dados
        cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)", 
                       (tipo, desc, valor, data))
        conn.commit()

        # Limpa os campos do formulário
        self.ent_desc.delete(0, "end")
        self.ent_valor.delete(0, "end")
        self.carregar()  # Atualiza a tabela e saldo

    # Função para excluir a transação selecionada
    def del_transacao(self):
        item = self.tree.focus()
        if not item:
            return
        trans_id = self.tree.item(item)["values"][0]
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (trans_id,))
        conn.commit()
        self.carregar()  # Atualiza a tabela e saldo

    # Função para carregar as transações e calcular o saldo
    def carregar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
        rows = cursor.fetchall()
        saldo = 0
        for r in rows:
            self.tree.insert("", "end", values=r)
            if r[1] == "Receita":
                saldo += r[3]
            else:
                saldo -= r[3]

        self.lbl_saldo.configure(text=f"Saldo: R$ {saldo:.2f}")  # Atualiza o saldo exibido

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Define o modo de aparência
    ctk.set_default_color_theme("blue")  # Define o tema de cor
    app = App()  # Cria a aplicação
    app.mainloop()  # Inicia o loop principal da