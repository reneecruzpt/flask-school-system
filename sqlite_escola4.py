import sqlite3
import os

# === Função para conectar à base de dados ===
def conectar_base(nome_base='escola.db'):
    conn = sqlite3.connect(nome_base)
    conn.execute("PRAGMA foreign_keys = ON")  # Ativa verificação de chaves estrangeiras
    return conn

# === Função para criar as tabelas ===
def criar_tabelas(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='estudantes';")
    existe = cursor.fetchone()

    if existe:
        print("⚠️ As tabelas já existem.")
        return

    cursor.execute("""
    CREATE TABLE estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        carga_horaria INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE inscricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudante_id INTEGER NOT NULL,
        curso_id INTEGER NOT NULL,
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
        FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
        UNIQUE(estudante_id, curso_id)
    );
    """)

    conn.commit()
    print("✅ Tabelas criadas com sucesso.")

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
        print("✅ Dados de exemplo inseridos.")
    except sqlite3.IntegrityError:
        print("⚠️ Os dados já existem ou há conflitos (e-mails duplicados, por exemplo).")

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
        print("✅ Inscrições registadas.")
    except sqlite3.IntegrityError:
        print("⚠️ Já existem inscrições iguais ou IDs inválidos.")

# === Função para listar as inscrições ===
def listar_inscricoes(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.nome AS estudante, c.nome AS curso
    FROM inscricoes i
    JOIN estudantes e ON i.estudante_id = e.id
    JOIN cursos c ON i.curso_id = c.id;
    """)
    resultados = cursor.fetchall()
    if resultados:
        print("📚 Lista de inscrições:")
        for row in resultados:
            print(f" - {row[0]} está inscrito(a) em {row[1]}")
    else:
        print("📭 Nenhuma inscrição encontrada.")

# === Função para eliminar curso ===
def eliminar_curso(conn):
    try:
        curso_id = int(input("Digite o ID do curso a eliminar: "))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE id = ?;", (curso_id,))
        conn.commit()
        if cursor.rowcount:
            print(f"🗑️ Curso com ID {curso_id} eliminado com sucesso.")
        else:
            print("⚠️ Curso não encontrado.")
    except ValueError:
        print("⚠️ ID inválido.")

# === Função para mostrar as tabelas existentes na base de dados ===
def mostrar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    if tabelas:
        print("📂 Tabelas existentes:")
        for tabela in tabelas:
            print(f" - {tabela[0]}")
    else:
        print("📭 Nenhuma tabela encontrada na base de dados.")

# === Função para eliminar tabela específica ===
def eliminar_tabela(nome_tabela, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela};")  # Elimina a tabela se existir
        conn.commit()
        print(f"🗑️ Tabela '{nome_tabela}' eliminada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Erro ao eliminar a tabela: {e}")

# === Função para eliminar o arquivo da base de dados ===
def eliminar_base(nome_base='escola.db'):
    try:
        if os.path.exists(nome_base):
            os.remove(nome_base)
            print(f"🗑️ Base de dados '{nome_base}' eliminada com sucesso.")
        else:
            print("⚠️ Base de dados não encontrada.")
    except Exception as e:
        print(f"⚠️ Erro ao eliminar a base de dados: {e}")

# === Menu interativo ===
def menu():
    nome_base = 'escola.db'
    conn = conectar_base(nome_base)
    while True:
        print("\n📘 MENU PRINCIPAL")
        print("1 - Criar tabelas")
        print("2 - Inserir dados de exemplo")
        print("3 - Inserir inscrições")
        print("4 - Listar inscrições")
        print("5 - Eliminar curso")
        print("6 - Ver tabelas existentes")
        print("7 - Eliminar tabela específica")
        print("8 - Eliminar base de dados")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

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
        elif opcao == "7":
            tabela = input("Digite o nome da tabela a eliminar: ")
            eliminar_tabela(tabela, conn)
        elif opcao == "8":
            confirmar = input("Tem certeza que deseja eliminar a base de dados? (s/n): ").lower()
            if confirmar == 's':
                conn.close()  # Fecha a conexão antes de apagar o arquivo
                eliminar_base(nome_base)
            else:
                print("Operação cancelada.")
        elif opcao == "0":
            print("👋 A sair do programa...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

    conn.close()

# === Executar o programa ===
if __name__ == '__main__':
    menu()
