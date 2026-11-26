from flask import Flask, render_template, request, redirect, url_for, session
from database import *
from models import *

app = Flask(__name__)
app.secret_key = 'essa_eh_minha_chave_secreta_para_criar_sessoes_de_usuario' #
@app.route('/', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = Usuario.autenticar(request.form.get('email'), request.form.get('senha'))
        if usuario:
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            session['user_email'] = usuario.email
            session['user_perfil'] = usuario.perfil
            
            if usuario.perfil == 'admin': return redirect(url_for('painel_admin'))
            elif usuario.perfil == 'aluno': return redirect(url_for('painel_alunos'))
        else:
            erro = "E-mail ou senha incorretos."
    return render_template('login.html', erro=erro)

@app.route('/admin', methods=['GET', 'POST'])
def painel_admin():
    if session.get('user_perfil') != 'admin': return redirect(url_for('login'))
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'cadastrar_usuario':
            Administrador.cadastrar_usuario(request.form['nome'], request.form['email'], request.form['senha'], request.form['perfil'])
        
        elif acao == 'deletar_usuario':
            Administrador.deletar_usuario(request.form['id'])

        elif acao == 'atualizar_usuario':
            Administrador.atualizar_usuario(request.form['id'],request.form['nome'], request.form['email'], request.form['senha'], request.form['perfil'])


    usuarios = Administrador.listar_usuarios()
    
    
    return render_template('admin.html', usuarios=usuarios, nome=session.get('user_nome'), id = session.get('user_id'))

@app.route('/admin', methods=['GET', 'POST'])
def painel_admin_Cursos():
    if session.get('user_perfil') != 'admin': return redirect(url_for('login'))
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'cadastrar_curso':
            Administrador.cadastrar_curso(request.form['nome'], request.form['carga_horaria'], request.form['professor_id'])
        
        elif acao == 'deletar_curso':
            Administrador.deletar_curso(request.form['id'])

        elif acao == 'atualizar_curso':
            Administrador.atualizar_curso(request.form['id'],request.form['nome'], request.form['carga_horaria'], request.form['professor_id'])

    cursos = Administrador.listar_cursos()

    return render_template('admin.html', cursos=cursos, nome=session.get('user_nome'), id = session.get('user_id'))

@app.route('/comum', methods=['GET', 'POST'])
def painel_aluno():
    if session.get('user_perfil') != 'comum': return redirect(url_for('login'))

    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'atualizar_DadosAluno':
            Aluno.alterar_DadosAluno(request.form['id'], request.form.get('nome'), request.form.get('email'))


            ##parte responsável por atualizar a sessão com os dados novos
            session["user_nome"] = request.form.get("nome")
            session["user_email"] = request.form.get("email")

        elif acao == 'DeletarContacomum':
            Aluno.DeletarContaAluno(request.form['id'])
            session.clear()
            return redirect(url_for('login'))
        
    return render_template('aluno.html', nome=session.get('user_nome'), email=session.get('user_email'), id=session.get('user_id'))

    



@app.route('/painel')
def painel():
    if session.get('user_perfil') == 'admin': return redirect(url_for('painel_admin'))

    elif session.get('user_perfil') == 'comum': return redirect(url_for('painel_aluno'))

@app.route('/loja')
def loja():
    if session.get('user_perfil') == 'admin': return redirect(url_for('painel_adminLOJA'))
    elif session.get('user_perfil') == 'comum': return redirect(url_for('painel_comumLOJA'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    criar_tabela_usuarios()
    criar_tabela_cursos()
    criar_tabela_horarios()
    criar_tabela_matriculas()

    preencher_dados_iniciais()
    app.run(debug=True)


