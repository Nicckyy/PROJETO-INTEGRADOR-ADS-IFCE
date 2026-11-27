
import database as db

class Usuario:
    def __init__(self, id_usuario, nome, email, perfil, matricula):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.perfil = perfil
        self.matricula = matricula


    @staticmethod
    def autenticar(email, senha):
        dados = db.autenticar_usuario(email,senha)
        if dados:
            id_u, nome, email, perfil, matricula = dados
            if perfil == 'admin': return Administrador(id_u, nome, email, perfil, matricula)
            elif perfil == 'aluno': return Aluno(id_u, nome, email, perfil, matricula)
        return None


class Administrador(Usuario):

    @staticmethod
    def cadastrar_usuario(nome, email, senha, perfil, matricula):
        return db.cadastrar_usuario(nome, email, senha, perfil, matricula) #True se o cadastro for bem-sucedido, False caso contrário

    @staticmethod
    def listar_usuarios():
        usuarios = db.listar_usuarios()
        return [Administrador(id, nome, email, perfil, matricula) for id, nome, email, perfil, matricula in usuarios]

    
    @staticmethod
    def deletar_usuario( id_usuario):
        return db.deletar_usuario(id_usuario) #True se a exclusão for bem-sucedida, False caso contrário
    @staticmethod
    def atualizar_usuario( id_usuario, nome, email,senha, perfil):
        return db.atualizar_usuario(id_usuario, nome, email, senha, perfil) #True se a atualização for bem-sucedida, False caso contrário
    @staticmethod
    def encontrar_usuario_por_id( id_usuario):
        dados = db.encontrar_usuario_por_id(id_usuario)
        if dados:
            id_u, nome, email, perfil = dados
            if perfil == 'admin': return Administrador(id_u, nome, email, perfil)
            elif perfil == 'comum': return Aluno(id_u, nome, email, perfil)
        return None

class Professor(Usuario):
    @staticmethod
    def listar_professores():
        professores = db.listar_usuarios()
        return [Administrador(id_u, nome, email, perfil, matricula)for id_u, nome, email, perfil, matricula in professores if perfil in ('professor')]

class Aluno(Usuario):
    @staticmethod
    def listar_alunos():
        alunos = db.listar_usuarios()
        return [Administrador(id_u, nome, email, perfil, matricula)for id_u, nome, email, perfil, matricula in alunos if perfil in ('aluno')]


class Curso:
    def __init__(self, id_curso, nome, carga_horaria, professor_id):
        self.id = id_curso
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.professor_id = professor_id


    @staticmethod
    def cadastrar_curso(nome, carga_horaria, professor_id):
        return db.cadastrar_curso(nome, carga_horaria, professor_id) #True se o cadastro for bem-sucedido, False caso contrário
    
    @staticmethod
    def listar_cursos():
        cursos = db.listar_cursos()
        return [Curso(id_c, nome, carga_horaria, professor_id) for id_c, nome, carga_horaria, professor_id in cursos]

    @staticmethod
    def deletar_curso(id_curso):
        return db.deletar_curso(id_curso) #True se a exclusão for bem-sucedida, False caso contrário

    def atualizar_curso(id_curso):
        pass