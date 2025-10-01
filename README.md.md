# 🌐 Lista de Contatos Online  

**Autor:** Jean Michell Ritter dos Santos  
**Disciplina:** Projeto Tecnológico  
**Data:** 2025  

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-3.1.2-orange?logo=flask) ![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)  

---

## 💡 Descrição do Projeto
O **Lista de Contatos Online** é um sistema web que permite aos usuários gerenciar seus contatos pessoais de forma simples e prática, oferecendo:  

- Cadastro e login seguro;  
- Adição, edição e exclusão de contatos;  
- Visualização de todos os contatos cadastrados;  
- Interface moderna e responsiva baseada em **Bootstrap 5**.

---

## ⚙️ Funcionalidades  

1. **Cadastro de Usuário**: cria uma conta com nome, e-mail e senha.  
2. **Login de Usuário**: acesso seguro utilizando sessões.  
3. **Gerenciamento de Contatos**: adicionar, editar, excluir e listar contatos vinculados ao usuário.  
4. **Interface Responsiva**: compatível com desktop e dispositivos móveis.  
5. **Navbar Fixa**: navegação fácil entre páginas principais e logout.

---

## 🛠 Tecnologias Utilizadas  

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python     | 3.12   | Linguagem principal |
| Flask      | 3.1.2  | Framework web |
| SQLite     | 3.x    | Banco de dados relacional |
| Bootstrap  | 5      | Interface responsiva e estilizada |

---

## 📂 Estrutura de Arquivos  

```
lista_contatos/
│
├── app.py                   # Código principal do sistema
├── create_db.py             # Script para criar o banco de dados
├── database.db              # Banco de dados SQLite
├── templates/               # Arquivos HTML
│   ├── index.html
│   ├── login.html
│   ├── cadastro_usuario.html
│   ├── contatos.html
│   └── form_contato.html
├── static/                  # CSS, JS, imagens (se houver)
├── venv/                    # Ambiente virtual (não versionar)
└── README.md                # Este arquivo
```

---

## 🚀 Como Executar o Projeto  

### Pré-requisitos
- Python 3  
- Pip  

### Passos

1. **Abrir terminal** e navegar até a pasta do projeto:
```bash
cd caminho/para/lista_contatos
```

2. **Criar e ativar ambiente virtual** (opcional):
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Git Bash (Windows)
source venv/Scripts/activate

# Ativar no Linux/Mac
source venv/bin/activate
```

3. **Instalar dependências**:
```bash
pip install flask
```

4. **Criar banco de dados** (caso não exista):
```bash
python create_db.py
```

5. **Rodar o sistema**:
```bash
python app.py
```

6. **Acessar no navegador**:
```
http://127.0.0.1:5000/
```

---

## 📌 Observações

- Sistema feito para **uso acadêmico**; o professor poderá rodar sem necessidade de configurações avançadas.  
- Todas as páginas utilizam **Bootstrap 5** para responsividade.  
- Para encerrar o servidor, pressione `Ctrl + C`.