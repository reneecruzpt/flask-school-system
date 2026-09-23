import sqlite3

# === Função para conectar à base de dados ===
def conectar_base(nome_base='escola.db'):
    """
    Cria ou abre uma base de dados SQLite.
    Retorna o objeto 'conn', que representa a conexão com a base de dados.
    """
    conn = sqlite3.connect(nome_base)  # conn é o objeto de conexão
    conn.execute("PRAGMA foreign_keys = ON")  # Ativa a verificação de chaves estrangeiras
    return conn

# === Função para criar as tabelas ===
def criar_tabelas(conn):
    """
    Cria as tabelas 'estudantes', 'cursos' e 'inscricoes' se ainda não existirem.
    """
    cursor = conn.cursor()  # cursor é o objeto que executa comandos SQL

    # Tabela de estudantes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- chave primária
        nome TEXT NOT NULL,                    -- nome do estudante
        email TEXT UNIQUE NOT NULL             -- email único
    );
    """)

    # Tabela de cursos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- chave primária
        nome TEXT NOT NULL,                    -- nome do curso
        carga_horaria INTEGER NOT NULL         -- duração do curso
    );
    """)

    # Tabela de inscrições
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inscricoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- chave primária
        estudante_id INTEGER NOT NULL,         -- chave estrangeira para estudantes
        curso_id INTEGER NOT NULL,             -- chave estrangeira para cursos
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id) ON DELETE CASCADE,
        FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
        UNIQUE(estudante_id, curso_id)         -- impede inscrições duplicadas
    );
    """)

    conn.commit()  # Confirma as alterações na base de dados

# === Função para inserir dados de exemplo nas tabelas principais ===
def inserir_dados_exemplo(conn):
    """
    Insere dados de exemplo nas tabelas 'estudantes' e 'cursos'.
    """
    cursor = conn.cursor()

    # Lista de estudantes a inserir
    estudantes = [
        ("Ana Souza", "ana@example.com"),
        ("Carlos Lima", "carlos@example.com")
    ]
    # Insere múltiplos estudantes com executemany
    cursor.executemany("INSERT INTO estudantes (nome, email) VALUES (?, ?);", estudantes)

    # Lista de cursos a inserir
    cursos = [
        ("Python Básico", 40),
        ("Flask Avançado", 30)
    ]
    # Insere múltiplos cursos
    cursor.executemany("INSERT INTO cursos (nome, carga_horaria) VALUES (?, ?);", cursos)

    conn.commit()

# === Função para inserir inscrições dos estudantes nos cursos ===
def inserir_inscricoes(conn):
    """
    Regista quais estudantes estão inscritos em quais cursos.
    """
    cursor = conn.cursor()

    inscricoes = [
        (1, 1),  # Ana em Python Básico
        (1, 2),  # Ana em Flask Avançado
        (2, 2)   # Carlos em Flask Avançado
    ]

    cursor.executemany("INSERT INTO inscricoes (estudante_id, curso_id) VALUES (?, ?);", inscricoes)
    conn.commit()

# === Função para listar as inscrições (JOIN entre tabelas) ===
def listar_inscricoes(conn):
    """
    Mostra os estudantes com os cursos em que estão inscritos.
    Utiliza JOIN entre as tabelas.
    """
    cursor = conn.cursor()

    cursor.execute("""
    SELECT e.nome AS estudante, c.nome AS curso
    FROM inscricoes i
    JOIN estudantes e ON i.estudante_id = e.id
    JOIN cursos c ON i.curso_id = c.id;
    """)

    print("📚 Inscrições:")
    for row in cursor.fetchall():
        print(f" - {row[0]} está inscrito(a) em {row[1]}")

# === Função para eliminar um curso e verificar a integridade referencial ===
def eliminar_curso(conn, curso_id):
    """
    Elimina um curso da tabela 'cursos'.
    Graças ao ON DELETE CASCADE, as inscrições associadas também são eliminadas.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cursos WHERE id = ?;", (curso_id,))
    conn.commit()
    print(f"🗑️ Curso com id {curso_id} foi eliminado juntamente com as inscrições associadas.")

# === Função principal ===
def main():
    """
    Executa todas as operações em sequência:
    cria a base, insere dados, lista inscrições, elimina um curso, lista novamente.
    """
    conn = conectar_base()         # Cria ou conecta à base de dados
    criar_tabelas(conn)            # Cria as tabelas
    inserir_dados_exemplo(conn)   # Insere estudantes e cursos
    inserir_inscricoes(conn)      # Regista as inscrições
    listar_inscricoes(conn)       # Mostra a lista de inscrições

    # Teste de exclusão de curso com ON DELETE CASCADE
    eliminar_curso(conn, 2)       # Elimina o curso com id 2 (Flask Avançado)
    listar_inscricoes(conn)       # Verifica se as inscrições também foram removidas

    conn.close()  # Fecha a ligação com a base de dados

# === Ponto de entrada do programa ===
if __name__ == '__main__':
    main()
