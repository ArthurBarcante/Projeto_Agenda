# Como o projeto funciona

O funcionamento do AIgenda pode ser entendido em tres passos.

Primeiro, a pessoa abre o sistema pelo navegador.

Depois, a interface mostra as paginas que ela pode usar, como login, painel, compromissos e perfil.

Em algumas partes do sistema, a tela de entrada aparece com o nome `signin`, mas para o usuario isso representa simplesmente a tela de login.

Por tras dessa interface existe uma parte responsavel por processar as regras do sistema.

Essa parte recebe os pedidos da tela, verifica o que precisa ser feito e conversa com o banco de dados.

O banco de dados guarda as informacoes importantes, como usuarios e compromissos.

O fluxo geral fica assim:

1. O usuario interage com a tela.
2. A tela envia uma requisicao para o sistema.
3. O sistema analisa a requisicao.
4. As informacoes sao lidas ou gravadas no banco.
5. A resposta volta para a tela.

Exemplo:

Quando uma pessoa tenta entrar no sistema, a tela envia os dados de acesso.

O sistema verifica esses dados.

Se estiver tudo certo, a pessoa pode seguir para a area interna.

Quando o projeto estiver mais completo, esse mesmo fluxo sera usado para criar, editar e acompanhar compromissos com mais automacao.