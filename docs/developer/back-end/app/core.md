# Core

A camada `back/app/core` contém funcionalidades transversais:

- `auth.py`: resolve usuário autenticado via Bearer token.
- `config.py`: lê variáveis de ambiente e valida configuração.
- `security.py`: hash e validação de senha, criação e decode de JWT.
