
import database as db

class Usuario:
    def __init__(self, id_usuario, nome, email, perfil):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.perfil = perfil

    @staticmethod
    def autenticar(email, senha):
        dados = db.autenticar_usuario(email,senha)
        if dados:
            id_u, nome, email, perfil = dados
            if perfil == 'admin': return Administrador(id_u, nome, email, perfil)
            elif perfil == 'aluno': return Aluno(id_u, nome, email, perfil)
        return None


class Administrador(Usuario):

    @staticmethod
    def cadastrar_usuario(nome, email, senha, perfil):
        return db.cadastrar_usuario(nome, email, senha, perfil) #True se o cadastro for bem-sucedido, False caso contrário
    @staticmethod
    def listar_usuarios():
        usuarios = db.listar_usuarios()
        return [Administrador(id_u, nome, email, perfil) if perfil == 'admin' else Aluno(id_u, nome, email, perfil) for id_u, nome, email, perfil in usuarios if perfil in ('admin', 'comum')]
    
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

    @staticmethod
    def cadastrar_curso(nome, carga_horaria, professor_id):
        return db.cadastrar_curso(nome, carga_horaria, professor_id) #True se o cadastro for bem-sucedido, False caso contrário



    
    @staticmethod
    def listar_cursos():
        cursos = db.listar_cursos()
        return [Administrador(id_c, nome, carga_horaria, professor_id) for id_c, nome, carga_horaria, professor_id in cursos]


class Aluno(Usuario):
    pass
   # @staticmethod
   # def alterar_DadosAluno(id_usuario, nome, email):
   #     return db.alterar_NomeEmail(id_usuario, nome, email) #True se a atualização for bem-sucedida, False caso contrário
   # def DeletarContaComum(id_usuario):
   #     return db.deletar_usuario(id_usuario)


class Produto:
    def __init__(self, id_produto, nome, preco, quantidade):
        self.id = id_produto
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def listar_produtos():
        produtos = db.listar_produtos()
        #return [Usuario(id_u, nome, email, perfil) for id_u, nome, email, perfil in usuarios if perfil != 'admin']  # Retorna uma lista de objetos Usuario, excluindo o administrador
        return [Produto(id_p, nome, preco, quantidade) for id_p, nome, preco, quantidade in produtos]

    @staticmethod
    def cadastrar_produto(nome, preco, quantidade):
        return db.cadastrar_produto(nome, preco, quantidade) #True se o cadastro for bem-sucedido, False caso contrário

    @staticmethod
    def deletar_produto(id_produto):
        return db.deletar_produto(id_produto) #True se a exclusão for bem-sucedida, False caso contrário
    @staticmethod
    def atualizar_produto(id_produto, nome, preco, quantidade):
        return db.atualizar_produto(id_produto, nome, preco, quantidade) #True se a atualização for bem-sucedida, False caso contrário
    @staticmethod
    def encontrar_produto_por_nome(nome_produto):
        return db.encontrar_produto_por_nome(nome_produto) 

