import sqlite3
from sqlite3 import Error

def conectar():
    try:
        return sqlite3.connect("teste.db") 
    except Error as e:
        print(e)
        return None
    
################TABELA USUÁRIO
def criar_tabela_usuarios():
    
    conn = conectar()

    if conn is None:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL,
                matricula INTEGER UNIQUE
            )
        """)

        conn.commit()
        print("Tabela de usuários criada com sucesso!")

    except Error as erro:
        print("Erro ao criar tabela:", erro)

    finally:
        conn.close()

###############TABELA CURSOS
def criar_tabela_cursos():
    conn = conectar()



    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL,
                professor_id INTEGER NOT NULL,

                FOREIGN KEY (professor_id)
                REFERENCES usuarios(id)
            )
        """)

        conn.commit()
        print("Tabela cursos criada com sucesso!")

    except Error as erro:
        print("Erro ao criar cursos:", erro)

    finally:
        conn.close()

#################TABELA HORÁRIO
def criar_tabela_horarios():
    # Estabelece a conexão com o banco
    conn = conectar()


    try:
        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Cria a tabela de horários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                curso_id INTEGER NOT NULL,
                dia_semana TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fim TEXT NOT NULL,

                CHECK (hora_fim > hora_inicio),

                FOREIGN KEY (curso_id)
                REFERENCES cursos(id)
            )
        """)

        # Salva as alterações no banco
        conn.commit()

        print("Tabela horarios criada com sucesso!")

    except Error as erro:

        print("Erro ao criar tabela horarios:", erro)

    finally:
        # Fecha a conexão com o banco
        conn.close()

###########TABELA MATRICULA
def criar_tabela_matriculas():
    conn = conectar()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,

                n1 REAL CHECK (n1 BETWEEN 0 AND 10),
                n2 REAL CHECK (n2 BETWEEN 0 AND 10),
                n3 REAL CHECK (n3 BETWEEN 0 AND 10),
                n4 REAL CHECK (n4 BETWEEN 0 AND 10),

                UNIQUE (aluno_id, curso_id),

                FOREIGN KEY (aluno_id)
                REFERENCES usuarios(id),

                FOREIGN KEY (curso_id)
                REFERENCES cursos(id)
            )
        """)
        conn.commit()
        print("Tabela matriculas criada com sucesso!")

    except Error as erro:
        print("Erro ao criar matriculas:", erro)

    finally:
        conn.close()



def encontrar_usuario_por_id(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, perfil FROM usuarios WHERE id = ?", (id_usuario,))
    dados = cursor.fetchone()
    conn.close()
    return dados


def atualizar_usuario(id_usuario, nome, email, senha, perfil):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET nome = ?, email = ?, senha = ?, perfil = ? WHERE id = ?", (nome, email, senha, perfil, id_usuario))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()  

###########CRUD CURSO
def cadastrar_curso(nome, carga_horaria, professor_id):
    conn = conectar()
    try:
        cursor = conn.cursor()

        # Verifica se o professor existe e possui o perfil correto
        cursor.execute("""
            SELECT id FROM usuarios
            WHERE id = ? AND perfil = ?
        """, (professor_id, "professor"))

        professor = cursor.fetchone()

        if professor is None:
            print("Professor não encontrado!")
            return False

        # Insere o curso no banco de dados
        cursor.execute("""
            INSERT INTO cursos (nome, carga_horaria, professor_id)
            VALUES (?, ?, ?)
        """, (nome, carga_horaria, professor_id))

        conn.commit()

        print("Curso cadastrado com sucesso!")
        return True

    except Error as erro:
        print("Erro ao cadastrar curso:", erro)
        return False
    finally:
        conn.close()

def deletar_curso(id_cursos):
    conn = conectar()
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM cursos WHERE id = ?", (id_cursos,))
    conn.commit()
    conn.close() 


def listar_cursos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, carga_horaria, professor_id FROM cursos")
    cursos = cursor.fetchall()
    conn.close()
    return cursos


##########################################




### acesso aos dados do banco de dados
def autenticar_usuario(email,senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, perfil, matricula FROM usuarios WHERE email = ? and senha=?", (email,senha))
    dados = cursor.fetchone()
    conn.close()
    return dados # retorna dados se o usuário for encontrado, caso contrário retorna None


def cadastrar_usuario(nome, email, senha, perfil, matricula):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha, perfil, matricula) VALUES (?, ?, ?, ?, ?)", (nome, email, senha, perfil, matricula))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

    
def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, perfil, matricula FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios  # Retorna a lista de usuários


def deletar_usuario(id_usuario): 
    try:
        conn = conectar()
        cursor = conn.cursor() 
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def atualizar_usuario(id_usuario, nome, email, senha, perfil):
    conn = conectar()
    cursor = conn.cursor()
    if senha=="":
        try:
            cursor.execute("UPDATE usuarios SET nome = ?, email = ?, perfil = ? WHERE id = ?", (nome, email, perfil, id_usuario))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    else:
        try:
            cursor.execute("UPDATE usuarios SET nome = ?, email = ?, senha = ?, perfil = ? WHERE id = ?", (nome, email, senha, perfil, id_usuario))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

def encontrar_usuario_por_id(id_usuario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, perfil FROM usuarios WHERE id = ?", (id_usuario,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario  # Retorna o usuário encontrado ou None se não encontrado

def alterar_NomeEmail(id_usuario, nome, email):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (nome, email, id_usuario))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()




### dados iniciais do banco de dados
def preencher_dados_iniciais():
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO usuarios (id, nome, email, senha, perfil, matricula) VALUES (1, 'Admin', 'admin@admin.com', 'admin', 'admin', 1)")
        cursor.execute("INSERT OR IGNORE INTO usuarios (id, nome, email, senha, perfil, matricula) VALUES (2, 'Professor', 'professor@professor.com', 'professor', 'professor', 2)")
        cursor.execute("INSERT OR IGNORE INTO cursos (id, nome, carga_horaria, professor_id) VALUES (1, 'Desenvolvimento Web', 60, 1)")
        conn.commit()
    except Error as e:
        print(e)                 
    finally:
        if conn:
            conn.close()