import sqlite3
import datetime

# Conexão com o banco de dados
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Criação da tabela de livros
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    disponivel INTEGER DEFAULT 1
)
''')

# Criação da tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Criação da tabela de empréstimos
cursor.execute('''
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER,
    usuario_id INTEGER,
    data_emprestimo TEXT,
    data_devolucao TEXT,
    devolvido INTEGER DEFAULT 0,
    FOREIGN KEY (livro_id) REFERENCES livros (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
)
''')

conn.commit()
print("Banco de dados criado com sucesso!")

# Funções de gerenciamento

def adicionar_livro(titulo, autor):
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (?, ?)", (titulo, autor))
    conn.commit()
    print(f"Livro '{titulo}' adicionado com sucesso!")

def adicionar_usuario(nome, email):
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    print(f"Usuário '{nome}' adicionado com sucesso!")

def emprestar_livro(livro_id, usuario_id):
    cursor.execute("SELECT disponivel FROM livros WHERE id = ?", (livro_id,))
    disponivel = cursor.fetchone()
    
    if disponivel and disponivel[0] == 1:
        data_emprestimo = datetime.date.today().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo) VALUES (?, ?, ?)",
                       (livro_id, usuario_id, data_emprestimo))
        cursor.execute("UPDATE livros SET disponivel = 0 WHERE id = ?", (livro_id,))
        conn.commit()
        print(f"Livro ID {livro_id} emprestado ao usuário ID {usuario_id} com sucesso!")
    else:
        print("Este livro não está disponível para empréstimo.")

def devolver_livro(emprestimo_id):
    data_devolucao = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute("UPDATE emprestimos SET data_devolucao = ?, devolvido = 1 WHERE id = ?", (data_devolucao, emprestimo_id))
    cursor.execute("SELECT livro_id FROM emprestimos WHERE id = ?", (emprestimo_id,))
    livro_id = cursor.fetchone()[0]
    cursor.execute("UPDATE livros SET disponivel = 1 WHERE id = ?", (livro_id,))
    conn.commit()
    print(f"Empréstimo ID {emprestimo_id} devolvido com sucesso!")

def listar_livros():
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    print("Lista de livros:")
    for livro in livros:
        status = "Disponível" if livro[3] == 1 else "Emprestado"
        print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Status: {status}")

def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    print("Lista de usuários:")
    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")

# Função de menu para interação

def menu():
    while True:
        print("\n----- Sistema de Gerenciamento de Biblioteca -----")
        print("1. Adicionar livro")
        print("2. Adicionar usuário")
        print("3. Emprestar livro")
        print("4. Devolver livro")
        print("5. Listar livros")
        print("6. Listar usuários")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Digite o título do livro: ")
            autor = input("Digite o autor do livro: ")
            adicionar_livro(titulo, autor)

        elif opcao == '2':
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")
            adicionar_usuario(nome, email)

        elif opcao == '3':
            livro_id = int(input("Digite o ID do livro: "))
            usuario_id = int(input("Digite o ID do usuário: "))
            emprestar_livro(livro_id, usuario_id)

        elif opcao == '4':
            emprestimo_id = int(input("Digite o ID do empréstimo: "))
            devolver_livro(emprestimo_id)

        elif opcao == '5':
            listar_livros()

        elif opcao == '6':
            listar_usuarios()

        elif opcao == '7':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o menu
menu()

# Fechar a conexão com o banco de dados
conn.close()
