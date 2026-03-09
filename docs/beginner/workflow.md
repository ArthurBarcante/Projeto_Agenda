# Fluxo de Uso (Passo a Passo)

Este documento mostra como uma pessoa usa o AIgenda no dia a dia.

## Visao geral do fluxo

```text
Entrar no sistema
      |
      v
Criar compromisso
      |
      v
Validacoes automaticas
(conflito, permissao, empresa)
      |
      v
Compromisso confirmado
      |
      v
Acompanhar rotina e desempenho
      |
      v
Evoluir com metas, niveis e sugestoes
```

## Jornada de um usuario iniciante

### Etapa 1 - Login

O usuario informa dados de acesso e entra no sistema.

O sistema valida:

- identidade (quem e voce),
- empresa (a qual tenant voce pertence),
- permissoes (o que voce pode fazer).

### Etapa 2 - Criacao de compromisso

Usuario preenche formulario:

- titulo,
- data e hora,
- participantes,
- descricao opcional.

### Etapa 3 - Verificacoes automáticas

Antes de salvar, o sistema checa:

1. se horario conflita com outro compromisso;
2. se usuario tem permissao para criar;
3. se dados pertencem a empresa correta;
4. se a mesma requisicao nao foi repetida (idempotencia).

Se houver erro, o usuario recebe mensagem clara e pode corrigir.

### Etapa 4 - Confirmacao e acompanhamento

Com tudo valido:

- compromisso e salvo,
- historico da acao e registrado,
- agenda e atualizada.

### Etapa 5 - Ajustes durante o ciclo

Depois da criacao, usuario pode:

- editar (quando permitido),
- cancelar (seguindo regras de estado),
- acompanhar status do compromisso.

## Fluxo simplificado de criacao

```text
[Preencher formulario]
        |
        v
[Enviar]
        |
        v
[Sistema valida regras]
   |            |
   |ok          |erro
   v            v
[Salva]     [Mostra motivo]
   |            |
   v            v
[Confirma]  [Usuario corrige]
```

## Fluxo da evolucao por fases

### Fase 1 no uso diario

Usuario organiza agenda sem conflitos e com seguranca.

### Fase 2 no uso diario

Usuario passa a ter metas e ve progresso em painel.

### Fase 3 no uso diario

Interface fica mais personalizada conforme maturidade.

### Fase 4 no uso diario

Sistema passa a sugerir melhorias automaticas com base no comportamento.

## Exemplo completo (historia curta)

Maria e coordenadora de equipe.

1. Maria entra no AIgenda.
2. Cria reuniao de planejamento para sexta, 09:00.
3. Inclui 4 participantes.
4. Sistema detecta que um participante ja tem reuniao nesse horario.
5. Maria ajusta para 10:00.
6. Sistema aprova e salva.
7. A reuniao aparece para todos os participantes.
8. No futuro, Maria acompanha desempenho e metas no painel.

Resultado: menos retrabalho, menos conflito, mais previsibilidade.

## Boas praticas para o usuario

- Sempre conferir participantes antes de confirmar.
- Descrever o objetivo da reuniao no titulo/descricao.
- Cancelar compromissos quando nao forem mais necessarios.
- Revisar periodicamente o painel de desempenho.

## Resumo rapido

O workflow do AIgenda foi pensado para ser:

- simples para comecar,
- seguro para operar,
- inteligente para evoluir com o tempo.
