from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

# Pasta para upload de fotos de contatos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------------
# Função para formatar telefone
# -------------------------------
def formatar_telefone(numero):
    """
    Recebe um número como string ou int (ex: 51983518862) 
    e retorna no formato (51) 9 8351-8862
    """
    numero = str(numero)  # garante que seja string
    if len(numero) == 11:  # formato com DDD + 9 + 8 dígitos
        return f"({numero[:2]}) {numero[2]} {numero[3:7]}-{numero[7:]}"
    elif len(numero) == 10:  # formato com DDD + 8 dígitos
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    else:
        return numero  # retorna como está se não tiver 10 ou 11 dígitos

# -------------------------------
# Inicializa banco de dados
# -------------------------------
def inicializar_banco():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela Usuario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        pergunta_seg TEXT,
        resposta_seg TEXT
    )
    ''')

    # Tabela Contato
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contato (
        id_contato INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL,
        observacao TEXT,
        id_usuario INTEGER NOT NULL,
        foto TEXT
    )
    ''')

    # Garante que coluna 'foto' existe (em bancos antigos)
    try:
        cursor.execute("ALTER TABLE Contato ADD COLUMN foto TEXT")
    except sqlite3.OperationalError:
        pass  # já existe

    conn.commit()
    conn.close()

inicializar_banco()

# -------------------------------
# Rotas principais
# -------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# Cadastro de usuário
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        pergunta_seg = request.form.get('pergunta_seg')
        resposta_seg = request.form.get('resposta_seg')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Usuario (nome, email, senha, pergunta_seg, resposta_seg) VALUES (?, ?, ?, ?, ?)",
                (nome, email, senha, pergunta_seg, resposta_seg)
            )
            conn.commit()
            conn.close()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash("Erro: Email já cadastrado!", "danger")
    
    return render_template('cadastro_usuario.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Usuario WHERE email = ? AND senha = ?", (email, senha)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('contatos'))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# -------------------------------
# Contatos
# -------------------------------
@app.route('/contatos')
def contatos():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Contato WHERE id_usuario = ?", (user_id,))
    contatos = cursor.fetchall()
    conn.close()

    # Formata o telefone
    contatos_formatados = []
    for c in contatos:
        c = list(c)
        c[2] = formatar_telefone(c[2])  # coluna telefone
        contatos_formatados.append(c)

    return render_template('contatos.html', contatos=contatos_formatados)

@app.route('/adicionar_contato', methods=['POST'])
def adicionar_contato():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    observacao = request.form['observacao']
    user_id = session['user_id']

    # Upload de foto
    foto = request.files.get('foto')
    foto_nome = None
    if foto and foto.filename != '':
        foto_nome = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_nome))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Contato (nome, telefone, email, observacao, id_usuario, foto) VALUES (?, ?, ?, ?, ?, ?)",
        (nome, telefone, email, observacao, user_id, foto_nome)
    )
    conn.commit()
    conn.close()

    # Pop-up só na aba de contatos
    flash("Contato adicionado com sucesso!", "success")
    return redirect(url_for('contatos'))

@app.route('/editar_contato/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Contato WHERE id_contato = ?", (id,))
    contato = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        observacao = request.form['observacao']

        # Upload foto
        foto = request.files.get('foto')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if foto and foto.filename != '':
            foto_nome = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_nome))
            cursor.execute(
                "UPDATE Contato SET nome=?, telefone=?, email=?, observacao=?, foto=? WHERE id_contato=?",
                (nome, telefone, email, observacao, foto_nome, id)
            )
        else:
            cursor.execute(
                "UPDATE Contato SET nome=?, telefone=?, email=?, observacao=? WHERE id_contato=?",
                (nome, telefone, email, observacao, id)
            )
        conn.commit()
        conn.close()

        flash("Contato atualizado com sucesso!", "success")
        return redirect(url_for('contatos'))

    # Formata telefone para exibir no form
    contato = list(contato)
    contato[2] = formatar_telefone(contato[2])

    return render_template('form_contato.html', titulo="Editar Contato", botao="Salvar", contato=contato)

@app.route('/excluir_contato/<int:id>')
def excluir_contato(id):
    if 'user_id' not in session:
        flash("Você precisa fazer login primeiro!", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Contato WHERE id_contato = ? AND id_usuario = ?", (id, user_id))
    conn.commit()
    conn.close()

    flash("Contato excluído com sucesso!", "success")
    return redirect(url_for('contatos'))

# -------------------------------
# Perfil do usuário
# -------------------------------
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, pergunta_seg, resposta_seg FROM Usuario WHERE id_usuario = ?", (user_id,))
    usuario = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        pergunta_seg = request.form['pergunta_seg']
        resposta_seg = request.form['resposta_seg']
        cursor.execute(
            "UPDATE Usuario SET nome=?, email=?, pergunta_seg=?, resposta_seg=? WHERE id_usuario=?",
            (nome, email, pergunta_seg, resposta_seg, user_id)
        )
        conn.commit()
        conn.close()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for('perfil'))

    conn.close()
    return render_template('perfil.html', usuario=usuario)

# -------------------------------
# Pergunta de segurança
# -------------------------------
@app.route('/definir_pergunta', methods=['GET', 'POST'])
def definir_pergunta():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    if request.method == 'POST':
        pergunta_seg = request.form['pergunta_seg']
        resposta_seg = request.form['resposta_seg']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Usuario SET pergunta_seg = ?, resposta_seg = ? WHERE id_usuario = ?",
            (pergunta_seg, resposta_seg, user_id)
        )
        conn.commit()
        conn.close()
        flash("Pergunta de segurança salva com sucesso!", "success")
        return redirect(url_for('contatos'))

    return render_template('pergunta_seg.html')

# -------------------------------
# Esqueci minha senha
# -------------------------------
@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, pergunta_seg FROM Usuario WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            session['reset_user_id'] = usuario[0]
            return redirect(url_for('responder_pergunta'))
        else:
            flash("Email não encontrado!", "danger")
    return render_template('esqueci_senha.html')

@app.route('/responder_pergunta', methods=['GET', 'POST'])
def responder_pergunta():
    if 'reset_user_id' not in session:
        return redirect(url_for('esqueci_senha'))

    user_id = session['reset_user_id']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta_seg, resposta_seg FROM Usuario WHERE id_usuario = ?", (user_id,))
    usuario = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        resposta = request.form['resposta']
        if resposta.lower() == usuario[1].lower():
            return redirect(url_for('nova_senha'))
        else:
            flash("Resposta incorreta!", "danger")

    return render_template('responder_pergunta.html', pergunta=usuario[0])

@app.route('/nova_senha', methods=['GET', 'POST'])
def nova_senha():
    if 'reset_user_id' not in session:
        return redirect(url_for('esqueci_senha'))

    user_id = session['reset_user_id']
    if request.method == 'POST':
        nova_senha = request.form['senha']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuario SET senha = ? WHERE id_usuario = ?", (nova_senha, user_id))
        conn.commit()
        conn.close()
        session.pop('reset_user_id', None)
        flash("Senha atualizada com sucesso! Faça login agora.", "success")
        return redirect(url_for('login'))
    return render_template('nova_senha.html')

# -------------------------------
# Rodar servidor
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
