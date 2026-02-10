# Projeto_Agenda

Sistema de Agendamento — Fundamentos Conceituais

Este documento consolida todo o planejamento conceitual do sistema de agendamento.
Ele reúne as decisões tomadas durante a fase de modelagem lógica e serve como base única e estável para o início da construção do projeto.

- Não define tecnologias, implementações ou soluções técnicas.
- Não antecipa expansões futuras.
- Tudo aqui é intencionalmente suficiente para começar a construir.

1. Propósito do Sistema

- Centralizar o controle de compromissos entre pessoas, tempo e regras, com o objetivo de:
      - Reduzir conflitos de agenda e sobreposição de horários
      - Padronizar processos de agendamento
      - Aumentar previsibilidade e organização operacional
      - Reduzir dependência de controle manual e comunicação informal
      - Criar confiança no processo de agendamento

- O sistema existe para organizar o tempo compartilhado.

2. Problemas que o Sistema Resolve

- Agendas conflitantes
- Sobreposição de horários
- Uso ineficiente do tempo disponível
- Falta de visibilidade de disponibilidade real
- Cancelamentos desorganizados
- Reagendamentos manuais e confusos
- Falta de histórico confiável de alterações
- Comunicação fragmentada entre envolvidos
- Processos não padronizados
- Erros humanos recorrentes

3. Contextos de Uso

- Exemplos de aplicação:
    
    - Clínicas (médica, odontológica, psicológica)
    - Prestadores de serviço (consultoria, manutenção, aulas, atendimentos individuais)
    - Empresas (salas de reunião, equipes internas, agendas compartilhadas)
    - O domínio é genérico, aplicável a qualquer cenário onde tempo compartilhado precisa ser coordenado.

4. Escopo Conceitual Inicial
   
- Dentro do escopo

    - Usuários e perfis bem definidos
    - Agendas individuais
    - Compromissos como entidade central
    - Regras básicas de agendamento
    - Histórico completo de ações
    - Nota / reputação automatizada

- Fora do escopo inicial

    - Integrações externas
    - Relatórios avançados
    - Automação complexa de decisões
    - Dashboards estratégicos
    - Itens fora do escopo não devem ser antecipados.

5. Elementos Centrais do Sistema

- O sistema se baseia em quatro elementos fundamentais:

  - Usuários
  - Tempo (Agenda)
  - Compromissos
  - Regras

- Esses elementos:

  - São independentes
  - São interligados
  - Não dependem de decisões técnicas

6. Usuários e Perfis
   
Usuário

- Usuário é:

  - Uma entidade identificável
  - Origem de toda ação no sistema
  - Responsável por decisões e efeitos gerados

- Usuário não é:
  
  - Um perfil em si
  - Um conjunto de permissões técnicas
  - Um ator genérico sem identidade
  - Não existe ação sem usuário.

Perfis

- Perfis são fixos:

  - Cliente / Solicitante
  - Profissional / Executor
  - Administrador do Sistema

- Um usuário possui um perfil principal.
- O sistema raciocina conceitualmente com base nesse perfil.

Responsabilidade por Perfil

- Cliente / Solicitante

  - Pode:

    - Criar compromissos pessoais
    - Solicitar compromissos profissionais
    - Solicitar cancelamento ou alteração dentro das regras
    - Visualizar seus próprios dados e histórico

  - Não pode:

    - Confirmar compromissos profissionais
    - Definir regras globais
    - Alterar agenda de terceiros

  - Responsabilidade:

    - Respeitar horários
    - Comunicar intenções

- Profissional / Executor

  - Pode:
    - Criar e editar compromissos pessoais ou profissionais
    - Confirmar ou rejeitar solicitações
    - Definir disponibilidade
    - Gerenciar sua agenda
    - Criar e administrar perfis de clientes sob sua responsabilidade

  - Não pode:

    - Alterar regras globais
    - Alterar dados sistêmicos
    - Alterar perfis que não estejam sob sua responsabilidade

  - Responsabilidade:

    - Cumprir compromissos
    - Manter agenda coerente

7. Agenda (Tempo e Disponibilidade)
   
O que é Agenda

- Agenda é:

  - A representação do tempo disponível de um usuário
  - Um limite físico para existência de compromissos
  - A base para validação de qualquer agendamento

- Agenda não é:

  - Histórico
  - Fluxo de uso
  - Conjunto de regras
  - Recurso compartilhado genérico

- Se não existe na agenda, não pode virar compromisso.

Propriedade da Agenda

- Toda agenda pertence a um usuário
- Profissionais possuem agenda operacional
- Clientes não oferecem tempo, apenas solicitam

Componentes da Agenda

- A agenda é composta apenas por:

  - Disponibilidade
    - Intervalos agendáveis definidos pelo dono
  - Indisponibilidade
    - Bloqueios explícitos (temporários ou recorrentes)
  - Ocupação
    - Intervalos consumidos por compromissos
    - Sempre derivados de compromissos

Unidade de Tempo

  - Compromissos ocupam intervalos contínuos
  - Todo intervalo possui início e fim claros
  - Dois intervalos não podem se sobrepor
    
- Isso é uma lei física do sistema, não uma regra opcional.
  
Fronteiras da Agenda

- Agenda pode:
  
  - Informar intervalos livres, ocupados ou bloqueados
  - Validar possibilidade temporal

- Agenda não pode:

  - Criar compromissos
  - Tomar decisões
  - Aplicar penalidades
  - Alterar estados

- Agenda responde perguntas, não toma decisões.

8. Compromisso
   
Papel no Sistema

- O compromisso é a unidade central do sistema.
  
- Ele conecta:
  
  - Usuários
  - Agenda
  - Regras
  - Histórico
  - Notificações
  - Nota / reputação

- Sem compromisso:

  - Agenda é apenas disponibilidade
  - Não há histórico relevante
  - Não existe base para avaliação de comportamento
    
Existência e Dependência

- Um compromisso sempre pertence a uma agenda
- Nunca existe fora do tempo
- Sempre possui um autor identificável
- Nunca é criado automaticamente

Autor e Responsabilidade

- Todo compromisso possui um autor.

- O autor:

  - Criou o compromisso
  - Permanece registrado para sempre no histórico

- Autor não implica poder absoluto.
- Poder de alteração depende da agenda afetada e do tipo de compromisso.

Tipos de Compromisso

- Compromisso pessoal

  - Criado por um usuário
  - Pertence apenas à sua agenda
  - Não exige outros envolvidos

- Compromisso profissional

  - Criado por profissional
  - Possui ao menos um cliente associado
  - Cliente visualiza, mas não edita
    
- Múltiplos envolvidos

  - Menção simples em observações ou
  - Compromisso compartilhado (todos visualizam)
  - Decisão funcional e consciente.

Tempo e Duração

- Todo compromisso possui:

  - Data
  - Hora de início
  - Duração

- Características:

  - Duração flexível
  - Ajustável
  - Intervalo contínuo
  - Sem sobreposição

9. Estados e Situações do Compromisso
    
Estados Operacionais

- Controlam existência e fluxo:

  - Rascunho
    - Compromisso em montagem, ainda não efetivado

  - Agendado
    - Compromisso válido, ocupando agenda

  - Cancelado
    - Compromisso encerrado sem execução

  - Regras:

    - Apenas um estado por vez
    - Estado define ações permitidas
    - Estado define ocupação da agenda

Situações Avaliativas

- Não alteram fluxo:

    - Solicitado – registro de intenção
    - Atrasado – calculado pelo sistema
    - Não compareceu
    - Concluído

- Regras:

  - Não substituem estados
  - Não ocupam agenda
  - Servem para histórico, nota e análise

Regras Fundamentais

- Estado encerra ou mantém existência
- Situação avalia comportamento
- Reagendamento não é estado nem situação
- Reagendar = alterar data/hora + registrar no histórico

10. Cancelamento
    
Separação Conceitual
- Solicitar cancelamento
  - Intenção
  - Gera histórico
  - Não altera estado
- Cancelar
  - Ação executiva
  - Muda estado para Cancelado
  - Remove da agenda
  - Encerra o compromisso
- Responsável pelo cancelamento é quem executa, não quem solicita.

Avaliação do Cancelamento

- Após o cancelamento, o compromisso pode receber resultado:

  - Cancelado dentro da regra
  - Cancelado fora da regra
    
- Estado encerra.
- Resultado avalia.

11. Histórico

- Toda ação relevante gera histórico.
  
- O histórico registra:
  - Quem fez
  - Quando fez
  - O que mudou
  - Qual o impacto

- Características:
  - Imutável
  - Nunca apagado
  - Base para auditoria, nota e decisões futuras

- Se não gera histórico, não existe conceitualmente.

12. Nota / Reputação

- Calculada automaticamente
- Baseada em comportamento real
- Nunca depende de estado
- Nunca depende de intenção isolada
- Depende exclusivamente de:

  - Resultados consolidados
  - Comportamento recorrente

- Influencia regras futuras.

13. Notificações

- Objetivo:

  - Reduzir falhas humanas
  - Aumentar previsibilidade

- Disparadas em:

  - Criação
  - Alteração
  - Cancelamento
  - Mudança de estado ou situação

- Momentos:

  - Imediato
  - Horas antes
  - Dias antes

14. Princípios de Sustentação

- O sistema pode começar simples:

  - Poucos perfis
  - Regras básicas
  - Agenda individual

- Mas deve ser pensado desde o início para:

  - Histórico longo
  - Crescimento de usuários
  - Complexidade gradual de regras

15. Riscos Tratados pelo Modelo

  - Estados inconsistentes
  - Agenda confusa
  - Cancelamentos ambíguos
  - Falta de rastreabilidade
  - Dependência de controle manual
    
-Esses riscos são mitigados pela estrutura conceitual definida aqui.
