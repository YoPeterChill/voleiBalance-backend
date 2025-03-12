# 🏐 Vôlei Balance - Balanceamento de Times de Vôlei

## 📖 Sobre o Projeto
O **Vôlei Balance** é um sistema para equilibrar times de vôlei de forma justa e randômica. Os jogadores fazem **check-in** para confirmar presença no jogo, e o sistema distribui os times de maneira equilibrada, levando em conta o nível de habilidade de cada jogador. O objetivo é evitar desbalanceamento nos times e garantir partidas mais competitivas!

---

## 🛠️ Tecnologias Utilizadas

- **Back-end**: FastAPI 🚀
- **Banco de Dados**: PostgreSQL 🛢️
- **ORM**: SQLAlchemy
- **Autenticação de Configurações**: Python-dotenv

---

## ⚙️ Configuração do Projeto

### 🔹 1. Clone o repositório
```sh
git clone https://github.com/seu-usuario/volei-balance.git
cd volei-balance
```

### 🔹 2. Crie um ambiente virtual e ative
```sh
python -m venv venv  # Criar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
```

### 🔹 3. Instale as dependências
```sh
pip install -r requirements.txt
```

### 🔹 4. Configure o banco de dados
1. **Crie um banco de dados PostgreSQL**
2. **Configure as credenciais no arquivo `.env`**:
```
DATABASE_URL=postgresql://usuario:senha@localhost/volei_balance
```

### 🔹 5. Execute a aplicação
```sh
uvicorn main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

Para acessar a documentação interativa (Swagger): **http://127.0.0.1:8000/docs** 📜

---

## 🚀 Endpoints Disponíveis

### ✅ **Jogadores**
- **Criar um jogador**: `POST /players/`
- **Listar jogadores**: `GET /players/`
- **Buscar jogador por ID**: `GET /players/{player_id}`
- **Atualizar nível de habilidade**: `PUT /players/{player_id}`
- **Deletar um jogador**: `DELETE /players/{player_id}`

### ✅ **Check-in**
- **Fazer check-in**: `POST /checkin/{player_id}`
- **Listar jogadores que fizeram check-in**: `GET /checkins/`

### ✅ **Balanceamento de Times**
- **Criar times balanceados**: `GET /balance-teams/`

---

## 🎯 Próximos Passos e Melhorias Futuras
- 📌 Criar um **front-end** para facilitar o uso da aplicação
- 📌 Implementar **autenticação** para diferentes usuários (administrador e jogadores)
- 📌 Salvar **histórico de partidas e times formados**

---

## 🤝 Contribuição
Se quiser contribuir com o projeto:
1. Faça um **fork** do repositório 🍴
2. Crie uma **branch** para sua feature (`git checkout -b minha-feature`)
3. Faça **commit** das alterações (`git commit -m 'Adicionando minha feature'`)
4. Faça um **push** para a branch (`git push origin minha-feature`)
5. Abra um **Pull Request** 🚀

---

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se livre para usá-lo e melhorá-lo! 🔥

