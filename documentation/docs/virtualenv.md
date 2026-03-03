# Página de Virtualenv

## O que é a virtualenv no projeto

A pasta `virtualenv/` guarda ambientes virtuais Python isolados do sistema operacional. Isso garante que o backend use versões estáveis e reproduzíveis de bibliotecas.

## Estrutura atual

```text
virtualenv/
├── .venv/
└── venv/
```

Ambos representam ambientes locais Python; normalmente apenas um é mantido como padrão, mas os dois podem existir durante transição/ajustes.

## Por que isso é importante

- Evita conflito de dependências globais da máquina.
- Padroniza execução de testes e migrações.
- Permite onboarding mais seguro para novos devs.

## Uso rápido

- Ativar: `source virtualenv/.venv/bin/activate`
- Instalar deps: `pip install -r config/requirements.txt`
- Desativar: `deactivate`

## Boas práticas

- Não versionar o conteúdo da virtualenv no Git.
- Recriar o ambiente ao mudar significativamente as dependências.
- Manter `requirements.txt` como fonte de verdade das libs Python do projeto.
