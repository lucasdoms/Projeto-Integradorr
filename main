import tkinter as tk
from tkinter import ttk
from tkinter import font
from ttkthemes import ThemedTk
from tkinter import PhotoImage, Toplevel
from PIL import Image, ImageTk, ImageOps
import sqlite3
from tkinter import messagebox
from tkcalendar import Calendar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime
import webbrowser


class MainApplication(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)

        self.set_theme("adapta")

        self.title("Sistema de Gerenciamento")
        self.geometry("700x500")

        image = Image.open('imagens/logo.png')

        image = ImageOps.contain(image, (66, 67))
        self.logo_image = ImageTk.PhotoImage(image)

        logo_label = tk.Label(self, image=self.logo_image)
        logo_label.image = self.logo_image
        logo_label.pack(anchor='nw', padx=15, pady=15)

        background_color = "#ECEFF1"
        button_color = "#ADD8E6"
        text_color = "black"

        style = ttk.Style(self)
        style.configure('TFrame', background=background_color)
        style.configure('TLabel', background=background_color,
                        foreground=text_color, font=('Dubai', 12))

        style.configure('Custom.TButton', font=('Dubai', 12),
                        background=button_color, foreground=text_color)

        style.map('Custom.TButton',
                  foreground=[('pressed', text_color), ('active', text_color)],
                  background=[('pressed', '!disabled', button_color),
                              ('active', button_color)],
                  highlightcolor=[('focus', button_color)],
                  relief=[('pressed', 'groove'), ('!pressed', 'ridge')])

        self.configure(background=background_color)

        self.init_db()

        welcome_frame = ttk.Frame(self)
        welcome_frame.pack(pady=(20, 2), fill='x', expand=True)
        welcome_label = ttk.Label(welcome_frame, text="Bem-Vindo ao seu sistema de gerenciamento",
                                  font=("Dubai", 18), background=background_color)
        welcome_label.pack()

        instruction_frame = ttk.Frame(self)
        instruction_frame.pack(pady=(2, 5), fill='x', expand=True)
        instruction_label = ttk.Label(instruction_frame, text="Escolha a opção que deseja:",
                                      font=("Dubai", 14), background=background_color)
        instruction_label.pack()

        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=2, fill='x', expand=True)

        buttons_info = [
            ("Realizar Venda", self.realizar_venda),
            ("Visualizar Estoque", self.visualizar_estoque),
            ("Visualizar Vendas", self.visualizar_vendas),
            ("Cadastrar Produto", self.cadastrar_produto),
            ("Gerar Relatório", self.gerar_relatorio),
            ("Caixa", self.caixa)
        ]

        grid_columns = 2

        for index, (text, command) in enumerate(buttons_info):
            row = index // grid_columns
            column = index % grid_columns
            button = ttk.Button(buttons_frame, text=text,
                                command=command, style='Custom.TButton')
            button.grid(row=row, column=column, padx=10, pady=5, sticky='ew')

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

    def init_db(self):

        self.conn = sqlite3.connect('gerenciamento.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id_produto INTEGER PRIMARY KEY,
                nome_produto TEXT NOT NULL,
                preço_produto REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                descrição TEXT
            );
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id_venda INTEGER PRIMARY KEY,
                nome_cliente TEXT NOT NULL,
                endereço TEXT NOT NULL,
                telefone TEXT NOT NULL,
                valor_venda REAL NOT NULL,
                metodo_de_pagamento TEXT NOT NULL,
                data_da_venda TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    class MainApplication(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title("Sistema de Gerenciamento de Vendas")
            self.geometry("800x600")
            self.initialize_ui()

        def initialize_ui(self):
            ttk.Button(self, text="Realizar Venda",
                       command=self.realizar_venda).pack(pady=10)

    def realizar_venda(self):
        venda_window = tk.Toplevel(self)
        venda_window.title("Realizar Venda")
        venda_window.geometry("700x500")

        # Cabeçalho
        ttk.Label(venda_window, text="Realizar Venda", font=("Dubai", 20)).grid(
            row=0, column=0, columnspan=4, pady=(0, 20))

        self.venda_entries = {}
        self.produtos_venda = []  # Lista para armazenar os produtos vendidos
        campos = [
            ('Nome', 1, 0),
            ('Telefone', 1, 2),
            ('Endereço', 2, 0),
            ('Data da Venda', 2, 2),
            ('Pagamento', 4, 0)
        ]

        for campo, linha, coluna in campos:
            ttk.Label(venda_window, text=f"{campo}:", anchor="w").grid(
                row=linha, column=coluna, sticky="w", padx=5, pady=10)
            if campo == 'Pagamento':
                combobox = ttk.Combobox(venda_window, width=30, values=[
                                        'À vista', 'A prazo'])
                combobox.grid(row=linha, column=coluna+1,
                              sticky="ew", padx=10, pady=10)
                combobox.set('À vista')
                self.venda_entries[campo] = combobox
            else:
                entry = ttk.Entry(venda_window, width=30)
                entry.grid(row=linha, column=coluna+1,
                           sticky="ew", padx=10, pady=10)
                self.venda_entries[campo] = entry

        # Campo de seleção de produto
        ttk.Label(venda_window, text="Produto:", anchor="w").grid(
            row=3, column=0, sticky="w", padx=5, pady=10)
        produto_combobox = ttk.Combobox(
            venda_window, width=30, values=self.obter_nomes_produtos())
        produto_combobox.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

        # Campo para quantidade do produto
        ttk.Label(venda_window, text="Quantidade:").grid(
            row=3, column=2, sticky="e", padx=5, pady=10)
        quantidade_entry = ttk.Entry(venda_window, width=10)
        quantidade_entry.grid(row=3, column=3, sticky="ew", padx=10, pady=10)

        ttk.Button(venda_window, text="Adicionar Produto", style='Custom.TButton',
                   command=lambda: self.adicionar_produto_venda(produto_combobox.get(), quantidade_entry.get())).grid(row=4, column=3, padx=10, pady=10)

        # Área para listar produtos adicionados
        self.lista_produtos_frame = ttk.Frame(venda_window)
        self.lista_produtos_frame.grid(row=5, column=0, columnspan=4, pady=10)
        self.atualizar_lista_produtos()

        ttk.Button(venda_window, text="Finalizar Venda", style='Custom.TButton',
                   command=self.finalizar_venda).grid(row=6, column=0, columnspan=4, pady=30)

    def obter_nomes_produtos(self):
        try:
            self.cur.execute(
                "SELECT nome_produto FROM produtos ORDER BY nome_produto")
            return [item[0] for item in self.cur.fetchall()]
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não foi possível obter a lista de produtos: {e}")
            return []

    def adicionar_produto_venda(self, produto, quantidade):
        try:
            quantidade = int(quantidade)
            if quantidade > 0:
                self.produtos_venda.append((produto, quantidade))
                self.atualizar_lista_produtos()
            else:
                messagebox.showerror(
                    "Erro", "Quantidade deve ser maior que zero.")
        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira uma quantidade válida.")

    def atualizar_lista_produtos(self):
        for widget in self.lista_produtos_frame.winfo_children():
            widget.destroy()
        for produto, quantidade in self.produtos_venda:
            ttk.Label(self.lista_produtos_frame,
                      text=f"{produto} x {quantidade}").pack()

    def finalizar_venda(self):
        nome_cliente = self.venda_entries['Nome'].get()
        endereco = self.venda_entries['Endereço'].get()
        telefone = self.venda_entries['Telefone'].get()
        metodo_pagamento = self.venda_entries['Pagamento'].get()
        data_venda = self.venda_entries['Data da Venda'].get()

        if not (nome_cliente and endereco and telefone and data_venda and self.produtos_venda):
            tk.messagebox.showerror(
                "Erro", "Por favor, preencha todas as informações necessárias.")
            return

        # Calcula o valor total da venda
        valor_total = 0
        for produto, quantidade in self.produtos_venda:
            self.cur.execute(
                "SELECT preço_produto FROM produtos WHERE nome_produto = ?", (produto,))
            preco_produto = self.cur.fetchone()[0]
            valor_total += preco_produto * quantidade

        # Insere a venda no banco de dados
        venda_info = (nome_cliente, endereco, telefone,
                      valor_total, metodo_pagamento, data_venda)
        self.cur.execute(
            "INSERT INTO vendas (nome_cliente, endereço, telefone, valor_venda, metodo_de_pagamento, data_da_venda) VALUES (?, ?, ?, ?, ?, ?)", venda_info)

        # ID da venda 
        id_venda = self.cur.lastrowid

        # Atualiza a quantidade de produtos no estoque e registra os detalhes da venda
        for produto, quantidade in self.produtos_venda:
            # Atualiza o estoque
            self.cur.execute(
                "UPDATE produtos SET quantidade = quantidade - ? WHERE nome_produto = ?", (quantidade, produto))

        # Confirma as transações
        self.conn.commit()

        self.produtos_venda.clear()
        self.atualizar_lista_produtos()
        for entry in self.venda_entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)

        tk.messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")

    def visualizar_estoque(self):
        estoque_window = tk.Toplevel(self)
        estoque_window.title("Estoque de Produtos")
        estoque_window.geometry("900x500")

        # Exibe os produtos em estoque
        columns = ('Id_produto', 'nome_produto',
                   'preço_produto', 'quantidade', 'descrição')
        estoque_tree = ttk.Treeview(
            estoque_window, columns=columns, show='headings')
        estoque_tree.pack(expand=True, fill='both')
        estoque_tree.heading('Id_produto', text='ID')
        estoque_tree.heading('nome_produto', text='Nome')
        estoque_tree.heading('preço_produto', text='Preço')
        estoque_tree.heading('quantidade', text='Quantidade')
        estoque_tree.heading('descrição', text='Descrição')

        estoque_tree.column('Id_produto', width=70)
        estoque_tree.column('nome_produto', width=200)
        estoque_tree.column('preço_produto', width=100)
        estoque_tree.column('quantidade', width=100)
        estoque_tree.column('descrição', width=300)

        # Busca dados dos produtos no bd
        self.cur.execute("SELECT * FROM produtos")
        rows = self.cur.fetchall()

        # Preenche o treeview
        for row in rows:
            estoque_tree.insert('', tk.END, values=row)

        scrollbar = ttk.Scrollbar(
            estoque_window, orient=tk.VERTICAL, command=estoque_tree.yview)
        estoque_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def visualizar_vendas(self):

        vendas_window = tk.Toplevel(self)
        vendas_window.title("Vendas Realizadas")
        vendas_window.geometry("900x500")

        # Exibe as vendas
        columns = ('id_venda', 'nome_cliente', 'endereço',
                   'telefone', 'valor_venda', 'data_da_venda')
        vendas_tree = ttk.Treeview(
            vendas_window, columns=columns, show='headings')
        # Ajustar conforme necessário
        vendas_tree.pack(expand=True, fill='both', side='left')

        # cabeçalhos
        for col in columns:
            vendas_tree.heading(col, text=col.replace('_', ' ').title())
            # Ajustar a largura conforme necessário
            vendas_tree.column(col, width=150)

        # Busca dados das vendas no bd
        self.cur.execute("SELECT * FROM vendas")
        vendas_rows = self.cur.fetchall()

        for row in vendas_rows:
            vendas_tree.insert('', tk.END, values=row, tags=('venda',))

        scrollbar = ttk.Scrollbar(
            vendas_window, orient='vertical', command=vendas_tree.yview)
        vendas_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def cadastrar_produto(self):

        cadastro_window = tk.Toplevel(self)
        cadastro_window.title("Cadastrar Produto")
        cadastro_window.geometry("700x500")

        cadastro_window.grid_columnconfigure(1, weight=1)
        cadastro_window.grid_columnconfigure(3, weight=1)

        titulo = ttk.Label(
            cadastro_window, text="Cadastro de Produto", font=("Dubai", 20))
        titulo.grid(row=0, column=0, columnspan=4, pady=20)

        self.produto_entries = {}
        campos = [
            ('nome_produto', 'Nome', 1, 0),
            ('Id_produto', 'ID_PRODUTO', 1, 2),
            ('preço_produto', 'Preço', 2, 0),
            ('quantidade', 'Quantidade', 2, 2),
            ('descrição', 'Descrição', 3, 0)
        ]

        for campo, label, row, col in campos:
            ttk.Label(cadastro_window, text=f"{label}:").grid(
                row=row, column=col, padx=10, pady=15, sticky="e")
            if campo == 'descrição':
                entry = tk.Text(cadastro_window, height=4, width=50)
                entry.grid(row=row, column=col+1, columnspan=3,
                           sticky="ew", padx=10, pady=15)
            else:
                entry = ttk.Entry(cadastro_window, width=20)
                entry.grid(row=row, column=col+1,
                           sticky="ew", padx=10, pady=15)
            self.produto_entries[campo] = entry
        save_button = ttk.Button(cadastro_window, text="CADASTRAR PRODUTO",
                                 style='Custom.TButton', command=self.salvar_produto)
        save_button.grid(row=10, column=0, columnspan=4, pady=60)

    def salvar_produto(self):
        dados_produto = {}
        for campo, widget in self.produto_entries.items():
            if campo == 'descrição':
                dados_produto[campo] = widget.get(
                    "1.0", "end-1c")
            else:
                dados_produto[campo] = widget.get()

        # Insere o novo produto no bd
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO produtos (id_produto, nome_produto, preço_produto, quantidade, descrição)
                    VALUES (?, ?, ?, ?, ?)
                """, (dados_produto['Id_produto'], dados_produto['nome_produto'], dados_produto['preço_produto'], dados_produto['quantidade'], dados_produto['descrição']))
            tk.messagebox.showinfo(
                "Sucesso", "Produto cadastrado com sucesso.")
        except Exception as e:
            tk.messagebox.showerror(
                "Erro", f"Não foi possível cadastrar o produto: {e}")
        finally:
            for widget in self.produto_entries.values():
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", "end")
                else:
                    widget.delete(0, tk.END)

    def gerar_relatorio(self):
        relatorio_window = tk.Toplevel(self)
        relatorio_window.title("Gerar Relatório")
        relatorio_window.geometry("700x500")

        background_color = "#ECEFF1"
        relatorio_window.configure(background=background_color)

        tk.Label(relatorio_window, text="Data de início:",
                 bg=background_color, fg="black").pack()
        inicio_cal = Calendar(relatorio_window, selectmode='day',
                              foreground='black',
                              background='white',
                              headersbackground='gray',
                              normalbackground=background_color,
                              weekendbackground='lightgray',
                              weekendforeground='black')
        inicio_cal.pack(pady=(10, 0))

        tk.Label(relatorio_window, text="Data de fim:",
                 bg=background_color, fg="black").pack()
        fim_cal = Calendar(relatorio_window, selectmode='day',
                           foreground='black',
                           background='white',
                           headersbackground='gray',
                           normalbackground=background_color,
                           weekendbackground='lightgray',
                           weekendforeground='black')
        fim_cal.pack(pady=(10, 20))
        ttk.Button(relatorio_window, text="Gerar Relatório", style='Custom.TButton',
                   command=lambda: self.criar_relatorio(
                       inicio_cal.get_date(), fim_cal.get_date())).pack(pady=(10, 10))

    def criar_relatorio(self, data_inicio, data_fim):
        # Converte e valida datas
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%d/%m/%Y')
            data_fim_obj = datetime.strptime(data_fim, '%d/%m/%Y')
        except ValueError as e:
            messagebox.showerror("Erro de Formato de Data",
                                 f"Erro ao formatar as datas: {e}")
            return

        # Formata para o padrão SQL
        data_inicio_sql = data_inicio_obj.strftime('%Y-%m-%d')
        data_fim_sql = data_fim_obj.strftime('%Y-%m-%d')

        # Consulta SQL para obter vendas no período
        self.cur.execute("""
            SELECT id_venda, nome_cliente, endereço, telefone, valor_venda, data_da_venda, metodo_de_pagamento 
            FROM vendas 
            WHERE data_da_venda BETWEEN ? AND ?""", (data_inicio_sql, data_fim_sql))
        vendas = self.cur.fetchall()

        # Verifica se há vendas no período
        if not vendas:
            messagebox.showinfo(
                "Relatório de Vendas", "Nenhuma venda encontrada para o período selecionado.")
            return

        # PDF
        relatorio_nome = f"relatorio_{data_inicio_sql.replace('-', '_')}_a_{data_fim_sql.replace('-', '_')}.pdf"
        c = canvas.Canvas(relatorio_nome, pagesize=letter)
        c.setFont("Helvetica", 10)
        c.drawString(
            100, 800, f"Relatório de Vendas de {data_inicio} a {data_fim}")
        c.drawString(
            100, 785, "ID | Cliente | Endereço | Telefone | Valor | Data | Pagamento")
        altura = 765
        for venda in vendas:
            venda_info = f"{venda[0]} | {venda[1]} | {venda[2]} | {venda[3]} | {venda[4]} | {venda[5]} | {venda[6]}"
            c.drawString(100, altura, venda_info)
            altura -= 15

        c.drawString(
            100, altura, f"Valor total: R$ {sum(venda[4] for venda in vendas):,.2f}")
        c.showPage()
        c.save()

        # Abre o relatório
        if os.path.exists(relatorio_nome):
            webbrowser.open(relatorio_nome)
        else:
            messagebox.showerror("Erro", "Falha ao gerar o relatório PDF.")

    def caixa(self):

        caixa_window = tk.Toplevel(self)
        caixa_window.title("Caixa")
        caixa_window.geometry("700x500")

        background_color = "#ECEFF1"
        caixa_window.configure(background=background_color)

        columns = ('id_venda', 'valor_venda')
        vendas_tree = ttk.Treeview(
            caixa_window, columns=columns, show='headings')
        vendas_tree.pack(expand=True, fill='both')

        vendas_tree.heading('id_venda', text='ID da Venda')
        vendas_tree.heading('valor_venda', text='Valor da Venda')
        self.cur.execute("SELECT id_venda, valor_venda FROM vendas")
        vendas_rows = self.cur.fetchall()

        for row in vendas_rows:
            vendas_tree.insert('', tk.END, values=row)

        total_vendas = sum(venda[1] for venda in vendas_rows)

        total_label = tk.Label(
            caixa_window, text=f"Total no Caixa: R${total_vendas:.2f}", bg=background_color, fg="black")
        total_label.pack(pady=10)


# Executar
app = MainApplication()
font.families()
app.mainloop()
