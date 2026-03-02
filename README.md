# PROJETO AGENDA - Sistema Inteligente de Organização e Evolução Pessoal (AIGENDA)

**Versão atual:** `0.1`  
**Tag:** `v0.1`

## Objetivo do sistema

O **AIGENDA** é um sistema digital para ajudar pessoas e equipes a organizarem sua rotina de forma inteligente, progressiva e adaptativa.

Não é apenas uma agenda tradicional. O sistema foi construído para:

- organizar compromissos com consistência estrutural;
- evitar conflitos de horário automaticamente;
- impedir sobreposição de tarefas;
- manter integridade organizacional;
- preparar base sólida para evolução comportamental e personalização futura.

## Princípio de autonomia

Desde o primeiro uso, o usuário mantém liberdade para criar, ajustar e cancelar compromissos.  
O sistema não bloqueia ações por nível: a evolução futura amplia personalização e profundidade, sem restringir autonomia.

## Estado atual do projeto

O AIGENDA está estruturado em fases evolutivas. Atualmente, a **Fase 1 - Organização Inteligente** está implementada.

Essa fase entrega:

- cadastro e edição de compromissos;
- múltiplos participantes;
- prevenção automática de conflitos;
- isolamento multi-tenant por empresa;
- controle de auditoria (apenas criador altera/cancela);
- máquina de estados segura.

## Arquitetura atual

- Arquitetura modular por domínio.
- Fluxo interno: Controllers (rotas) -> Services (regras de negócio) -> Repository/ORM -> Models (domínio).
- Separação de responsabilidades aplicada entre API, serviços, domínio e persistência.

## Tecnologias utilizadas

- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Alembic
- Python-JOSE (JWT)
- Passlib (bcrypt)
- Pytest
- Python-dotenv

## Documentação

- [Status do projeto (o que foi feito até agora)](docs/o-que-foi-feito-ate-agora.md)
- [Funcionalidades atuais](docs/funcionalidades-atuais.md)
- [Funcionalidades futuras (roadmap)](docs/funcionalidades-futuras.md)

## Repositório

- GitHub: https://github.com/ArthurBarcante/Projeto_Agenda
