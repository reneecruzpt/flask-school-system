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
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- identifica unicamente cada estudante, gerado automaticamente
        nome TEXT NOT NULL,                     -- nome do estudante, campo obrigatório
        email TEXT UNIQUE NOT NULL              -- email deve ser único e não pode ser nulo
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- identifica unicamente cada curso, autoincrementado
        nome TEXT NOT NULL,                     -- nome do curso, obrigatório
        carga_horaria INTEGER NOT NULL          -- duração do curso em horas, obrigatório
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inscricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- identificador único da inscrição
        estudante_id INTEGER NOT NULL,          -- referência ao estudante, obrigatório
        curso_id INTEGER NOT NULL,              -- referência ao curso, obrigatório
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,  -- se estudante for removido, elimina inscrições relacionadas
        FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,          -- se curso for removido, elimina inscrições relacionadas
        UNIQUE(estudante_id, curso_id)          -- impede que o mesmo estudante se inscreva duas vezes no mesmo curso
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

    # Consulta SQL que seleciona o nome do estudante e do curso,
    # juntando as tabelas inscricoes, estudantes e cursos.
    cursor.execute("""
    SELECT 
        e.nome AS estudante,  -- seleciona o nome do estudante
        c.nome AS curso       -- seleciona o nome do curso
    FROM 
        inscricoes i          -- tabela principal: inscrições
    JOIN 
        estudantes e ON i.estudante_id = e.id  -- junta estudantes pelo id do estudante
    JOIN 
        cursos c ON i.curso_id = c.id          -- junta cursos pelo id do curso
    ;
    """)

    resultados = cursor.fetchall()  # recupera todos os registros retornados pela consulta

    if resultados:
        print("📚 Lista de inscrições:")
        for row in resultados:
            # row[0] contém o nome do estudante, row[1] o nome do curso
            print(f" - {row[0]} está inscrito(a) em {row[1]}")
    else:
        print("📭 Nenhuma inscrição encontrada.")


# === Função para eliminar curso ===
def eliminar_curso(conn):
    try:
        curso_id = int(input("Digite o ID do curso a eliminar: "))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE id = ?;", (curso_id,))  # elimina curso pelo id
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # busca nomes de tabelas no esquema do banco
    tabelas = cursor.fetchall()
    if tabelas:
        print("📂 Tabelas existentes:")
        for tabela in tabelas:
            print(f" - {tabela[0]}")
    else:
        print("📭 Nenhuma tabela encontrada na base de dados.")

# === Menu interativo ===
def menu():
    conn = conectar_base()
    while True:
        print("\n📘 MENU PRINCIPAL")
        print("1 - Criar tabelas")
        print("2 - Inserir dados de exemplo")
        print("3 - Inserir inscrições")
        print("4 - Listar inscrições")
        print("5 - Eliminar curso")
        print("6 - Ver tabelas existentes")
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
        elif opcao == "0":
            print("👋 A sair do programa...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")
            
        input("pressione enter para continuar")
    conn.close()

# === Executar o programa ===
if __name__ == '__main__':
    menu()