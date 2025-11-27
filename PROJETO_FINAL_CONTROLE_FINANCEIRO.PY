# CÓDIGO COM EXPLICAÇÃO, PARA QUE TODOS POSSAM ENTENDER #

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter


# BANCO DE DADOS:

def conectar(): # Conectando no banco
    return sqlite3.connect('gastos_credito.db')

def criar_tabela(): # Criando a tabela
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gastos_credito (
            descricao   TEXT,
            responsavel TEXT,
            valor       REAL
        )
    ''')
    conn.commit()
    conn.close()


# FUNÇÕES:

def inserir_gasto(): # Função que insere o dado
    descricao = descricao_entry.get().strip()
    responsavel = responsavel_entry.get().strip()
    valor = valor_entry.get().strip()

    if descricao and responsavel and valor:
        try:
            valor_float = float(valor.replace(',', '.'))

            conn = conectar()
            c = conn.cursor()
            c.execute("INSERT INTO gastos_credito VALUES (?, ?, ?)",
                      (descricao, responsavel, valor_float))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Gasto inserido com sucesso!")
            
            mostrar_gastos()

        except ValueError:
            messagebox.showwarning("Erro", "O valor deve ser numérico.")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def mostrar_gastos(): # Função que exibe os dados
    for item in tree.get_children(): ######################
        tree.delete(item)

    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM gastos_credito")
    linhas = c.fetchall()
    conn.close()

    for descricao, responsavel, valor in linhas:
        tree.insert("", "end", values=(descricao, responsavel, f"{valor:.2f}"))

def carregar_selecao(event): # deixa em evidencia o que foi clicado
    selecao = tree.selection()
    if selecao:
        valores = tree.item(selecao)['values']
        descricao, responsavel, valor = valores

        descricao_entry.insert(0, descricao)
        responsavel_entry.insert(0, responsavel)
        valor_entry.insert(0, valor)

def atualizar_gasto(): # Função que atualiza os valores
    selecao = tree.selection()
    if not selecao:
        messagebox.showwarning("Atenção", "Selecione um item na tabela.")
        return

    descricao_antiga = tree.item(selecao)['values'][0]

    nova_desc = descricao_entry.get().strip()
    novo_resp = responsavel_entry.get().strip()
    novo_valor = valor_entry.get().strip()

    if nova_desc and novo_resp and novo_valor:
        try:
            valor_float = float(novo_valor.replace(',', '.'))

            conn = conectar()
            c = conn.cursor()
            c.execute("""
                UPDATE gastos_credito
                SET descricao = ?, responsavel = ?, valor = ?
                WHERE descricao = ?
            """, (nova_desc, novo_resp, valor_float, descricao_antiga))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Gasto atualizado!")
            
            mostrar_gastos()

        except ValueError:
            messagebox.showwarning("Erro", "O valor deve ser numérico.")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def deletar_gasto(): #Função que deleta a linha selecionada
    selecao = tree.selection()
    if not selecao:
        messagebox.showwarning("Atenção", "Selecione um item.")
        return

    descricao_del = tree.item(selecao)['values'][0]

    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM gastos_credito WHERE descricao = ?", (descricao_del,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Gasto deletado!")
    
    mostrar_gastos()

def calcular_total_responsavel(): #Função que soma o valor total do nome inserido
    nome = responsavel_entry.get().strip()
    if not nome:
        messagebox.showwarning("Atenção", "Digite o nome do responsável.")
        return

    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT SUM(valor) FROM gastos_credito WHERE responsavel = ?", (nome,))
    total = c.fetchone()[0]
    conn.close()

    if total is None:
        total = 0.0

    label_total_valor.config(text=f"R$ {total:.2f}")


# LAYOUT DA JANELA: 

customtkinter.set_appearance_mode("black") #configura o 'tema' da janela (claro/escuro)
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()
janela.title("Controle de Débitos do Cartão")
janela.geometry("700x500")
caminho = 'icone_para_proj_final.ico'
janela.iconbitmap(caminho)

# TITULO DA JANELA
titulo_label = tk.Label(
    janela,
    text="LISTA DE DÉBITOS DO CARTÃO",
    font=("Arial", 16, "bold")
)
titulo_label.grid(row=0, column=0, columnspan=3, pady=10)

# CAMPOS PARA PREENCHIMENTO:

tk.Label(janela, text="Descrição da compra:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)

descricao_entry = tk.Entry(janela, font=("Arial", 12), width=30)
descricao_entry.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=5)


tk.Label(janela, text="Quem realizou:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)

responsavel_entry = tk.Entry(janela, font=("Arial", 12), width=20)
responsavel_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)


tk.Label(janela, text="Valor (R$):", font=("Arial", 12)).grid(row=3, column=0, sticky="e", padx=5, pady=5)

valor_entry = tk.Entry(janela, font=("Arial", 12), width=10)
valor_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)


# CRIAÇÃO DA TABELA:
colunas = ("DESCRIÇÃO", "RESPONSÁVEL", "VALOR")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=10) #tree +-= tabela
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=150)


# BOTÕES:

btn_salvar = customtkinter.CTkButton(janela, text="SALVAR", command=inserir_gasto)
btn_salvar.grid(row=4, column=0, padx=5, pady=10)

btn_atualizar = customtkinter.CTkButton(janela, text="ATUALIZAR", command=atualizar_gasto)
btn_atualizar.grid(row=4, column=1, padx=5, pady=10)

btn_deletar = customtkinter.CTkButton(janela, text="DELETAR", command=deletar_gasto)
btn_deletar.grid(row=4, column=2, padx=5, pady=10)

# CLIQUE DA LINHA: (SEM ELE TODOS OS ITENS SAO ALTERADOS)
tree.bind("<<TreeviewSelect>>", carregar_selecao)

# SOMA TOTAL DE CADA RESPONSAVEL:
btn_total = customtkinter.CTkButton(janela, text="Total do responsável", command=calcular_total_responsavel)
btn_total.grid(row=6, column=0, padx=5, pady=10)

label_total_texto = tk.Label(janela, text="Total gasto:", font=("Arial", 12))
label_total_texto.grid(row=6, column=1, sticky="e")

label_total_valor = tk.Label(janela, text="R$ 0,00", font=("Arial", 12, "bold"), fg="red")
label_total_valor.grid(row=6, column=2, sticky="w")


# Chama as funções e mantem a tela aberta :)

criar_tabela()
mostrar_gastos()

janela.mainloop()
