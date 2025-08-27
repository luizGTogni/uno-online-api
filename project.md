# Uno Online com WebSockets

- Conexão em Realtime
- Autenticação
- Gestão de Salas (Rooms)
- Convite (Link) / Código para entrar
- Persistência de estado no servidor
- Boa Arquitetura

## Base Inicial

### Stack (Tecnologias)
- FastAPI (HTTP + WebSocket)
- SQLAlchemy + Alembic (Migrations)
- Postgres
- Redis (Rooms)
- Docker Composer (Subir Postgres, Redis e App)
- JWT
- Pydantic
- Tests (Pytest + Coverage)
- Pylint + Pre commit
- Github Actions (Lint + Test)

### Requisitos

#### Usuários
[ ] Usuário deve conseguir logar na sua conta com email + senha.
[ ] Usuário deve conseguir criar conta com os campos: nome, username, email, senha, created_at, updated_at.
[ ] Usuário deve conseguir resetar sua senha via e-mail. (Envio de Email usar Rabbit MQ)
[ ] Usuário deve conseguir atualizar seus dados (ex: nome, avatar, username).
[ ] Usuário deve ter token de autenticação (JWT) para acessar rotas privadas.

#### Salas & Convites
[ ] Usuário autenticado deve conseguir criar uma sala (definir nome da sala, número máximo de jogadores).
[ ] Ao criar a sala, o sistema deve gerar um código único (ex: ABCD12) e um link de convite. (Redis)
[ ] Usuário deve conseguir entrar em uma sala existente via código ou link. (Redis)
[ ] Usuário deve conseguir sair de uma sala. (Redis)
[ ] O dono da sala deve conseguir expulsar jogadores / Banir jogador. (Atualizar Redis)
[ ] O sistema deve fechar automaticamente a sala quando o jogo terminar. (Redis TTL)
[ ] O sistema deve passar o dono da sala para o próximo (Atualizar Redis)

#### WebSocket & Interações
[ ] Usuário deve conseguir conectar ao WebSocket após entrar na sala. (FastApi WebSocket)
[ ] Sistema deve enviar broadcast de eventos para todos os jogadores da sala (ex: "João entrou", "Maria saiu"). 
[ ] Usuários devem conseguir enviar mensagens no chat da sala.
[ ] O jogo deve começar apenas quando todos os jogadores marcarem “pronto”. (Redis)

### Regras do Jogo (UNO)
- O sistema deve embaralhar e distribuir 7 cartas para cada jogador no início da partida. (Memoria / Redis (Escalável))
- O sistema deve manter um baralho de compra e uma pilha de descarte.
- O jogador da vez deve conseguir jogar uma carta válida (mesmo número, cor ou símbolo).
- Caso não tenha carta válida, o jogador deve comprar uma carta do baralho.
- O sistema deve validar automaticamente jogadas inválidas e rejeitá-las.
- O sistema deve gerenciar ordem dos turnos (incluindo efeitos de +2, +4, inverter, pular).
- O sistema deve declarar vencedor quando um jogador ficar sem cartas.
- O sistema deve impedir que o jogador esqueça de falar UNO (opcional: botão de UNO).

### Qualidade & Observabilidade
- Todas as funcionalidades devem ter testes unitários (pytest).
- Serviços críticos (login, criação de sala, jogadas) devem ter testes de integração.
- O sistema deve registrar logs estruturados (ex: logging).
- sistema deve expor um endpoint de healthcheck (/health).
- Monitoramento do Jogo (Prometheus / Grafana)

### Estrutura de pastas
uno-online/
│── src/
│   ├── app/                # Entrypoint da API
│   │   ├── main.py         # FastAPI app
│   │   ├── routes/         # Rotas HTTP e WebSocket
│   │   └── dependencies.py
│   │
│   ├── core/               # Configurações e middlewares
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Banco de dados (CRUD)
│   ├── services/           # Regras de negócio (UserService, RoomService, GameEngine)
│   ├── game/               # Lógica do UNO (deck, cartas, turnos, engine)
│   └── tests/              # pytest
│
│── alembic/                # Migrações do DB
│── docker-compose.yml
│── pyproject.toml / requirements.txt
│── .env

### Fluxo de interação
- Usuário cria conta (HTTP → UserService → Postgres).
- Usuário cria sala (HTTP → RoomService → Postgres + Redis p/ cache da sala).
- Outros entram pelo código/link (HTTP + validação JWT).
- Ao entrar, abre conexão WebSocket (entra no “canal da sala”).
- Servidor distribui cartas (GameEngine roda no Redis p/ suportar múltiplos workers).
- Jogadores enviam jogadas via WS → engine valida → broadcast p/ todos os players.