import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar tabela usuário com pergunta e resposta de segurança
cursor.execute('''
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    pergunta_seg TEXT,        -- nova coluna
    resposta_seg TEXT         -- nova coluna
)
''')

# Criar tabela contato
cursor.execute('''
CREATE TABLE IF NOT EXISTS Contato (
    id_contato INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    observacao TEXT,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
)
''')

conn.commit()
conn.close()
print("Banco criado/atualizado com sucesso!")
