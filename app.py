from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Necessário para sessões

# -------------------------------
# Rotas
# -------------------------------

# Página inicial
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

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Erro: Email já cadastrado!"
    
    return render_template('cadastro_usuario.html')

# Login de usuário
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
            return "Email ou senha incorretos!"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Página de contatos
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
    return render_template('contatos.html', contatos=contatos)

# Adicionar contato
@app.route('/adicionar_contato', methods=['GET', 'POST'])
def adicionar_contato():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        observacao = request.form['observacao']
        user_id = session['user_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Contato (nome, telefone, email, observacao, id_usuario) VALUES (?, ?, ?, ?, ?)",
            (nome, telefone, email, observacao, user_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('contatos'))

    return render_template('form_contato.html', titulo="Adicionar Contato", botao="Adicionar", contato=None)

# Editar contato
@app.route('/editar_contato/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Contato WHERE id_contato = ?", (id,))
    contato = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        observacao = request.form['observacao']

        cursor.execute(
            "UPDATE Contato SET nome = ?, telefone = ?, email = ?, observacao = ? WHERE id_contato = ?",
            (nome, telefone, email, observacao, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('contatos'))

    conn.close()
    return render_template('form_contato.html', titulo="Editar Contato", botao="Salvar", contato=contato)

# Excluir contato
@app.route('/excluir_contato/<int:id>')
def excluir_contato(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Contato WHERE id_contato = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('contatos'))

# -------------------------------
# Rodar o servidor
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
