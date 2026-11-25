import database






database.criar_tabela_usuarios()
database.criar_tabela_cursos()

database.cadastrar_usuarios(
    "Professor Teste",
    "professor@teste.com",
    "123456",
    "professor",
    None
)

# Mostra os usuários cadastrados
usuarios = database.listar_usuarios()

for usuario in usuarios:
    print(usuario)

resultado = database.cadastrar_curso(
    "Python Básico",
    40,
    1
)

print("Resultado:", resultado)
