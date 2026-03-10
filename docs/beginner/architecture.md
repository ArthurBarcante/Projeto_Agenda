# Como as Partes do Sistema se Conectam

## Visao simples

O AIgenda tem dois blocos:

- parte visual (frontend), que voce abre no navegador;
- parte de regras (backend), que decide o que pode ou nao pode.

Tambem existem dois apoios:

- banco de dados (PostgreSQL), onde as informacoes ficam salvas;
- cache de controle (Redis), usado para limitar excesso de requisicoes.

## Caminho de uma acao

```text
Pessoa no navegador
  -> Tela do sistema (frontend)
  -> Requisicao para API (backend)
  -> Validacoes de seguranca e regras
  -> Gravacao no banco
  -> Resposta volta para a tela
```

## Explicando sem termos complicados

- Frontend: o que o usuario enxerga e clica.
- Backend: o que verifica as regras e salva os dados.
- Banco de dados: memoria de longo prazo do sistema.
- Redis: ajuda a proteger a API de excesso de chamadas.

## Por que essa separacao e importante

- facilita manutencao;
- melhora seguranca;
- ajuda o sistema a crescer sem virar bagunca.
