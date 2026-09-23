import sqlite3

# === Função para conectar à base de dados ===
def conectar_base(nome_base='escola.db'):
    conn = sqlite3.connect(nome_base)
    conn.execute("PRAGMA foreign_keys = ON")  # Ativa verificação de chaves estrangeiras
    return conn

# === Função para criar as tabelas ===
def criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        carga_horaria INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inscricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudante_id INTEGER NOT NULL,
        curso_id INTEGER NOT NULL,
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
        FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
        UNIQUE(estudante_id, curso_id)
    );
    """)

    conn.commit()
    print("✅ Tabelas criadas com sucesso.")  # Linha nova: confirmação visual da criação

# === Função para inserir dados de exemplo ===
def inserir_dados_exemplo(conn):
    cursor = conn.cursor()

    estudantes = [
        ("Ana Souza", "ana@example.com"),
        ("Carlos Lima", "carlos@example.com")
    ]
    cursos = [
        ("Python Básico", 40),
        ("Flask Avançado", 30)
    ]

    try:
        cursor.executemany("INSERT INTO estudantes (nome, email) VALUES (?, ?);", estudantes)
        cursor.executemany("INSERT INTO cursos (nome, carga_horaria) VALUES (?, ?);", cursos)
        conn.commit()
        print("✅ Dados de exemplo inseridos.")  # Linha nova: mensagem de sucesso
    except sqlite3.IntegrityError:
        print("⚠️ Os dados já existem ou há conflitos (e-mails duplicados, por exemplo).")  # Linha nova: mensagem de erro

# === Função para inserir inscrições ===
def inserir_inscricoes(conn):
    cursor = conn.cursor()

    inscricoes = [
        (1, 1),
        (1, 2),
        (2, 2)
    ]

    try:
        cursor.executemany("INSERT INTO inscricoes (estudante_id, curso_id) VALUES (?, ?);", inscricoes)
        conn.commit()
        print("✅ Inscrições registadas.")  # Linha nova: confirmação visual
    except sqlite3.IntegrityError:
        print("⚠️ Já existem inscrições iguais ou IDs inválidos.")  # Linha nova: mensagem de erro

# === Função para listar as inscrições ===
def listar_inscricoes(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.nome AS estudante, c.nome AS curso
    FROM inscricoes i
    JOIN estudantes e ON i.estudante_id = e.id
    JOIN cursos c ON i.curso_id = c.id;
    """)
    resultados = cursor.fetchall()  # Linha nova: guarda resultados para verificar se há dados
    if resultados:  # Linha nova: verifica se há dados antes de mostrar
        print("📚 Lista de inscrições:")
        for row in resultados:
            print(f" - {row[0]} está inscrito(a) em {row[1]}")
    else:
        print("📭 Nenhuma inscrição encontrada.")  # Linha nova: mensagem caso não existam inscrições

# === Função para eliminar curso ===
def eliminar_curso(conn):
    try:
        curso_id = int(input("Digite o ID do curso a eliminar: "))  # Linha nova: pede input do utilizador para o ID do curso
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE id = ?;", (curso_id,))
        conn.commit()
        if cursor.rowcount:  # Linha nova: verifica se alguma linha foi afetada
            print(f"🗑️ Curso com ID {curso_id} eliminado com sucesso.")  # Linha nova: confirmação de sucesso
        else:
            print("⚠️ Curso não encontrado.")  # Linha nova: alerta se ID não existir
    except ValueError:
        print("⚠️ ID inválido.")  # Linha nova: trata erro de input não numérico

# === Função para mostrar as tabelas existentes na base de dados ===
def mostrar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # Linha nova: consulta tabelas SQLite
    tabelas = cursor.fetchall()  # Linha nova: guarda lista de tabelas
    if tabelas:  # Linha nova: verifica se há tabelas
        print("📂 Tabelas existentes:")
        for tabela in tabelas:
            print(f" - {tabela[0]}")  # Linha nova: mostra cada tabela
    else:
        print("📭 Nenhuma tabela encontrada na base de dados.")  # Linha nova: mensagem se base vazia

# === Menu interativo ===
def menu():
    conn = conectar_base()  # Linha nova: conecta base ao iniciar menu
    while True:
        print("\n📘 MENU PRINCIPAL")
        print("1 - Criar tabelas")
        print("2 - Inserir dados de exemplo")
        print("3 - Inserir inscrições")
        print("4 - Listar inscrições")
        print("5 - Eliminar curso")
        print("6 - Ver tabelas existentes")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")  # Linha nova: recebe escolha do utilizador

        if opcao == "1":
            criar_tabelas(conn)
        elif opcao == "2":
            inserir_dados_exemplo(conn)
        elif opcao == "3":
            inserir_inscricoes(conn)
        elif opcao == "4":
            listar_inscricoes(conn)
        elif opcao == "5":
            eliminar_curso(conn)
        elif opcao == "6":
            mostrar_tabelas(conn)
        elif opcao == "0":
            print("👋 A sair do programa...")  # Linha nova: mensagem de saída
            break  # Linha nova: sai do loop e termina o menu
        else:
            print("❌ Opção inválida. Tente novamente.")  # Linha nova: mensagem para entrada inválida

    conn.close()  # Linha nova: fecha conexão ao sair do menu

# === Executar o programa ===
if __name__ == '__main__':
    menu()  # Linha nova: inicia menu ao executar o script
