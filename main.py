import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3
import tkinter.messagebox
from tkcalendar import Calendar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


class MainApplication(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)

        self.set_theme("equilux")  # tema

        self.title("Sistema de Gerenciamento")
        self.geometry("700x500")

        style = ttk.Style(self)
        style.configure('White.TButton', font=('Arial', 12),
                        foreground='white', padding=[15, 10])

        background_color = "#474747"
        self.configure(background=background_color)

        # Inicialização do bd
        self.init_db()

        welcome_frame = ttk.Frame(self, style="TFrame")
        welcome_frame.pack(pady=(20, 2), fill='x', expand=True)
        welcome_label = ttk.Label(welcome_frame, text="Bem-Vindo ao seu sistema de gerenciamento",
                                  font=("Arial", 16, 'bold'), background=background_color, foreground="white")
        welcome_label.pack()

        instruction_frame = ttk.Frame(self, style="TFrame")
        instruction_frame.pack(pady=(2, 5), fill='x', expand=True)
        instruction_label = ttk.Label(instruction_frame, text="Escolha a opção que deseja:",
                                      font=("Arial", 12, 'bold'), background=background_color, foreground="white")
        instruction_label.pack()

        buttons_frame = ttk.Frame(self, style="TFrame")
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
                                command=command, style='White.TButton')
            button.grid(row=row, column=column, padx=10, pady=5, sticky='ew')

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

    def init_db(self):
        # Cria uma conexão com o banco de dados
        self.conn = sqlite3.connect('gerenciamento.db')
        self.cur = self.conn.cursor()
        # Cria as tabelas 
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

    def realizar_venda(self):
        # Cria uma nova janela
        venda_window = tk.Toplevel(self)
        venda_window.title("Realizar Venda")
        venda_window.geometry("600x400")
        background_color = "#474747"

        # Adicionando campos de entrada para os detalhes da venda
        campos = [
            ('Nome do Cliente', None),
            ('Endereço', None),
            ('Telefone', None),
            ('Método de Pagamento', ['À vista', 'A prazo']),
            ('Data da Venda', None)
        ]

        self.venda_entries = {}
        for i, (label, options) in enumerate(campos):
            frame = ttk.Frame(venda_window)
            frame.pack(pady=5)
            ttk.Label(frame, text=label + ":").pack(side=tk.LEFT)
            if options:
                combo = ttk.Combobox(frame, values=options)
                combo.pack(side=tk.RIGHT, expand=True, fill=tk.X)
                combo.set(options[0])
                self.venda_entries[label] = combo
            else:
                entry = ttk.Entry(frame)
                entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
                self.venda_entries[label] = entry

        # Área para adicionar produtos
        produto_frame = ttk.Frame(venda_window)
        produto_frame.pack(pady=10)
        ttk.Label(produto_frame, text="Produto:").pack(side=tk.LEFT)
        self.produto_entry = ttk.Combobox(
            produto_frame, values=self.obter_nomes_produtos())
        self.produto_entry.pack(side=tk.LEFT)
        ttk.Label(produto_frame, text="Quantidade:").pack(side=tk.LEFT)
        self.quantidade_entry = ttk.Entry(produto_frame)
        self.quantidade_entry.pack(side=tk.LEFT)
        ttk.Button(produto_frame, text="Adicionar",
                   command=self.adicionar_produto_venda).pack(side=tk.LEFT)

        # Mostrar produtos adicionados e o valor total
        self.lista_produtos_frame = ttk.Frame(venda_window)
        self.lista_produtos_frame.pack(pady=5)
        # Lista para manter controle dos produtos adicionados
        self.produtos_venda = []
        self.atualizar_lista_produtos()

        # Finalizar a venda
        ttk.Button(venda_window, text="Finalizar Venda",
                   command=self.finalizar_venda).pack(pady=5)

    def obter_nomes_produtos(self):
        self.cur.execute("SELECT nome_produto FROM produtos")
        return [item[0] for item in self.cur.fetchall()]

    def adicionar_produto_venda(self):
        produto = self.produto_entry.get()
        quantidade = self.quantidade_entry.get()
        if produto and quantidade.isdigit():
            self.produtos_venda.append((produto, int(quantidade)))
            self.atualizar_lista_produtos()
        else:
            print("Por favor, insira um produto e uma quantidade válida.")

    def atualizar_lista_produtos(self):
        # Limpar a lista atual de produtos
        for widget in self.lista_produtos_frame.winfo_children():
            widget.destroy()
        # Adicionar os produtos atuais à lista
        for produto, quantidade in self.produtos_venda:
            ttk.Label(self.lista_produtos_frame,
                      text=f"{produto} x {quantidade}").pack()

    def finalizar_venda(self):
        # Informações da venda
        nome_cliente = self.venda_entries['Nome do Cliente'].get()
        endereco = self.venda_entries['Endereço'].get()
        telefone = self.venda_entries['Telefone'].get()
        metodo_pagamento = self.venda_entries['Método de Pagamento'].get()
        data_venda = self.venda_entries['Data da Venda'].get()

        # Verifica se todas as informações necessárias foram fornecidas
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

        # ID da venda criada
        id_venda = self.cur.lastrowid

        # Atualiza a quantidade de produtos no estoque e registrar os detalhes da venda
        for produto, quantidade in self.produtos_venda:
            # Atualiza o estoque
            self.cur.execute(
                "UPDATE produtos SET quantidade = quantidade - ? WHERE nome_produto = ?", (quantidade, produto))

        # Confirma as transações
        self.conn.commit()

        # Limpa a interface da venda
        self.produtos_venda.clear()
        self.atualizar_lista_produtos()
        for entry in self.venda_entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('')
            else:
                entry.delete(0, tk.END)

        tk.messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")

    def visualizar_estoque(self):
        # Cria uma nova janela
        estoque_window = tk.Toplevel(self)
        estoque_window.title("Estoque de Produtos")
        estoque_window.geometry("900x600")  # Ajuste conforme necessário

        # Adiciona um treeview para exibir os produtos em estoque
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

        # Preenche o treeview com os dados dos produtos
        for row in rows:
            estoque_tree.insert('', tk.END, values=row)

        scrollbar = ttk.Scrollbar(
            estoque_window, orient=tk.VERTICAL, command=estoque_tree.yview)
        estoque_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def visualizar_vendas(self):
        # Cria uma nova janela
        vendas_window = tk.Toplevel(self)
        vendas_window.title("Vendas Realizadas")
        vendas_window.geometry("1000x600")  # Ajuste conforme necessário

        # Adiciona um Treeview para exibir as vendas realizadas
        columns = ('id_venda', 'nome_cliente', 'endereço',
                   'telefone', 'valor_venda', 'data_da_venda')
        vendas_tree = ttk.Treeview(
            vendas_window, columns=columns, show='headings')
        vendas_tree.pack(expand=True, fill='both', side='left')

        # Definir os cabeçalhos do Treeview
        for col in columns:
            vendas_tree.heading(col, text=col.replace('_', ' ').title())
            # Ajustar a largura conforme necessário
            vendas_tree.column(col, width=150)

        # Busca dados das vendas no bd
        self.cur.execute("SELECT * FROM vendas")
        vendas_rows = self.cur.fetchall()

        # Preenchee o Treeview com os dados das vendas
        for row in vendas_rows:
            vendas_tree.insert('', tk.END, values=row, tags=('venda',))

        scrollbar = ttk.Scrollbar(
            vendas_window, orient='vertical', command=vendas_tree.yview)
        vendas_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        vendas_tree.bind('<<TreeviewSelect>>', self.exibir_detalhes_venda)

        # Exibe os detalhes dos produtos de uma venda selecionada
        self.detalhes_venda_frame = ttk.Frame(vendas_window)
        self.detalhes_venda_frame.pack(expand=True, fill='both', side='right')
        self.detalhes_venda_label = ttk.Label(
            self.detalhes_venda_frame, text="Detalhes da Venda", font=('Arial', 12, 'bold'))
        self.detalhes_venda_label.pack()

    def exibir_detalhes_venda(self, event):
        for widget in self.detalhes_venda_frame.winfo_children():
            widget.destroy()  # Limpa o frame de detalhes para a nova seleção

        selected_item = event.widget.selection()
        if selected_item:  # Verifica se algum item está selecionado
            item = event.widget.item(selected_item)
            id_venda = item['values'][0]  # Pega o ID da venda selecionada

            ttk.Label(self.detalhes_venda_frame, text=f"Detalhes da Venda {id_venda}", font=(
                'Arial', 12, 'bold')).pack()

            # Busca os produtos vendidos nessa venda específica
            self.cur.execute("""
                SELECT nome_produto, quantidade 
                FROM itens_venda
                JOIN produtos ON itens_venda.id_produto = produtos.id_produto
                WHERE id_venda = ?""", (id_venda,))
            produtos = self.cur.fetchall()

            # Verifica se há produtos para essa venda
            if produtos:
                for nome_produto, quantidade in produtos:
                    ttk.Label(self.detalhes_venda_frame,
                              text=f"{nome_produto} - Quantidade: {quantidade}").pack()
            else:
                ttk.Label(self.detalhes_venda_frame,
                          text="Nenhum produto encontrado para esta venda.").pack()

    def cadastrar_produto(self):
        # Cria uma nova janela
        cadastro_window = tk.Toplevel(self)
        cadastro_window.title("Cadastrar Produto")
        cadastro_window.geometry("700x500")  # Ajuste conforme necessário
        background_color = "#474747"

        # Campos de formulário para as informações do produto
        campos = ['Id_produto', 'nome_produto',
                  'preço_produto', 'quantidade', 'descrição']
        self.produto_entries = {}
        for i, campo in enumerate(campos):
            frame = ttk.Frame(cadastro_window, style="TFrame")
            frame.pack(pady=5, fill='x', expand=True)
            label = ttk.Label(frame, text=campo + ":",
                              background=background_color, foreground="white")
            label.pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.produto_entries[campo] = entry

        cadastro_window.configure(background=background_color)

        # Botão para salvar o novo produto
        save_button = ttk.Button(
            cadastro_window, text="Salvar Produto", command=self.salvar_produto)
        save_button.pack(pady=20)
        for widget in [cadastro_window, save_button] + list(self.produto_entries.values()):
            widget.configure(background=background_color)

    def salvar_produto(self):
        # Coleta os dados do formulário
        dados_produto = {campo: entry.get()
                         for campo, entry in self.produto_entries.items()}

        # Insere o novo produto no banco de dados
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
            # Limpa os campos do formulário
            for entry in self.produto_entries.values():
                entry.delete(0, tk.END)

    def gerar_relatorio(self):
        relatorio_window = tk.Toplevel(self)
        relatorio_window.title("Gerar Relatório")
        relatorio_window.geometry("300x200")

        background_color = "#474747"
        relatorio_window.configure(background=background_color)

        tk.Label(relatorio_window, text="Data de início:",
                 bg=background_color, fg="white").pack()
        inicio_cal = Calendar(relatorio_window, selectmode='day')
        inicio_cal.pack()

        tk.Label(relatorio_window, text="Data de fim:",
                 bg=background_color, fg="white").pack()
        fim_cal = Calendar(relatorio_window, selectmode='day')
        fim_cal.pack()

        ttk.Button(relatorio_window, text="Gerar Relatório", command=lambda: self.criar_relatorio(
            inicio_cal.get_date(), fim_cal.get_date())).pack()

    def criar_relatorio(self, data_inicio, data_fim):
        # Formatando as datas
        data_inicio_formatada = data_inicio.replace('/', '-')
        data_fim_formatada = data_fim.replace('/', '-')

        self.cur.execute("""
            SELECT id_venda, nome_cliente, endereço, telefone, valor_venda, data_da_venda, metodo_de_pagamento 
            FROM vendas 
            WHERE data_da_venda BETWEEN ? AND ?""", (data_inicio, data_fim))
        vendas = self.cur.fetchall()

        # Calcula o valor total das vendas no período
        valor_total = sum([venda[4] for venda in vendas])

        # Gera o relatório PDF
        relatorio_nome = f"relatorio_{data_inicio_formatada}_a_{data_fim_formatada}.pdf"
        c = canvas.Canvas(relatorio_nome, pagesize=letter)
        c.drawString(
            100, 750, f"Relatório de Vendas de {data_inicio} a {data_fim}")
        c.drawString(
            100, 730, "ID Venda | Nome Cliente | Endereço | Telefone | Valor | Data | Método de Pagamento")
        altura = 710
        for venda in vendas:
            c.drawString(100, altura, str(venda))
            altura -= 20

        c.drawString(100, altura, f"Valor total das vendas: {valor_total}")
        c.save()

        # Abre o relatório gerado após a criação
        if os.path.exists(relatorio_nome):
            os.startfile(relatorio_nome)
        else:
            tk.messagebox.showinfo(
                "Erro", "Não foi possível gerar o relatório.")

    def caixa(self):
        # Cria uma nova janela
        caixa_window = tk.Toplevel(self)
        caixa_window.title("Caixa")
        caixa_window.geometry("400x300")

        background_color = "#474747"
        caixa_window.configure(background=background_color)

        # Adiciona um Treeview para exibir as vendas realizadas
        columns = ('id_venda', 'valor_venda')
        vendas_tree = ttk.Treeview(
            caixa_window, columns=columns, show='headings')
        vendas_tree.pack(expand=True, fill='both')

        # Define os cabeçalhos do Treeview
        vendas_tree.heading('id_venda', text='ID da Venda')
        vendas_tree.heading('valor_venda', text='Valor da Venda')

        # Busca os dados das vendas no bd
        self.cur.execute("SELECT id_venda, valor_venda FROM vendas")
        vendas_rows = self.cur.fetchall()

        # Preenche com os dados 
        for row in vendas_rows:
            vendas_tree.insert('', tk.END, values=row)

        # Calcula o valor total das vendas
        total_vendas = sum(venda[1] for venda in vendas_rows)

        # Mostra o valor total
        total_label = tk.Label(
            caixa_window, text=f"Total no Caixa: R${total_vendas:.2f}", bg=background_color, fg="white")
        total_label.pack(pady=10)


# Executa a aplicação
app = MainApplication()
app.mainloop()
