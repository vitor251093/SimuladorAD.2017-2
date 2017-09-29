# Simulador

## Enunciado

Neste trabalho, o aluno terá de executar a simulação do comportamento de um sistema no qual duas filas disputam o servidor, e uma das filas tem prioridade preemptiva sobre a outra (um serviço de menor prioridade, uma vez começado, pode ser interrompido pela chegada de um freguês de maior prioridade). Este serviço interrompido será terminado posteriormente, do ponto onde parou.

Fregueses chegam à fila 1 segundo um Processo Poisson com taxa ƛ (tempo entre chegadas é exponencial com taxa ƛ). Esta é a fila de maior prioridade do sistema. Após serem servidos pela primeira vez, os fregueses seguem para a fila 2, de menor prioridade, onde serão servidos por uma segunda vez. Ao término deste segundo serviço, os fregueses vão embora.

Tanto o primeiro como o segundo serviço do freguês são obtidos de forma independente a partir de uma distribuição exponencial com taxa µ = 1(s^-1). Isto significa que os serviços recebidos por um mesmo freguês são totalmente independentes, não guardando nenhuma relação entre eles.

Todavia, o serviço em andamento da fila 2 pode ser interrompido pela chegada de um freguês na fila 1. Neste caso, o serviço interrompido será retomado de onde parou. Observe que um freguês da fila 2 poderá ser interrompido mais de uma vez. Quando o freguês da fila 2 é interrompido, ele passa a ser o primeiro na fila de espera da fila 2.

As filas operam em regime FCFS (first come first serve - o primeiro a chegar é o primeiro a ser servido).

Os fregueses aguardando na fila 2 só são colocados em serviço, quando não há nenhum freguês em espera na fila 1. 

## Etapas

### 1. Introdução (10 pontos)

Descreva com detalhes a implementação do simulador, explicando:

- Funcionamento geral do simulador;
- Os eventos escolhidos;
- Estruturas internas utilizadas;
- A forma de geração das variáveis aleatórias envolvidas (facilidades de geração de número aleatório da linguagem utilizada); mostre como a semente é escolhida;
- Tipo de linguagem utilizada;
- Método usado: replicativo ou batch;
- Indicar como implementou o conceito de cores ou equivalência;
- Explicação da escolha dos parâmetros utilizados nas rodadas da simulação e tabela com os valores utilizados para cada cenário e para cada utilização (número de fregueses coletados por rodada, número de rodadas, tamanho da fase transiente, etc.). Estes dados podem também serem apresentados a cada resultado da simulação do item 4.
- Indique a máquina utilizada e a duração dos experimentos que levaram ao fator mínimo (explicado a frente)
- Outras informações pertinentes

### 2. Teste de Correção (10 pontos)

Nesta seção você descreverá os testes de correção que foram efetuados para garantir o pleno funcionamento do simulador. Você deve demonstrar que o seu programa está simulando exatamente e com correção o esquema proposto. Fórmulas analíticas não podem ser utilizadas para garantir a correção. Servem apenas de orientação, pois na maioria das vezes partimos para a simulação exatamente por não termos os resultados analíticos.

Procure rodar o simulador com cenários determinísticos com estatística conhecida, demonstrando que o programa está correto.

Você deverá anexar comentários sobre a boa qualidade dos intervalos de confiança obtidos e como os valores exatos se encaixam nestes intervalos, para os diversos valores de p.

### 3. Estimativa de fase transiente (10 pontos)

Nesta seção você descreverá como a fase transiente foi estimada para os diversos valores de  (obviamente existirá uma métrica mais crítica). A fase transiente deve sempre implicar num certo número de eventos de partida que são desprezados, esperando que o sistema entre em equilíbrio. Este número de partidas em cada cenário e para cada valor de utilização deve ser documentado, qualquer que seja o método escolhido para determinar o fim da fase transiente. 

A determinação da fase transiente é obrigatória, pois é um exercício para determinar a entrada em equilíbrio do sistema. Você terá que justificar suas escolhas. Este é um processo empírico, mas as dicas na apostila ajudam. 

Apresente resultados quantitativos que justificam sua escolha. Se você usou o método batch, além da estimação da fase transiente, mostre como as estatísticas entre as rodadas foram coletadas. 

Procure demonstrar a influência da escolha da fase transiente na qualidade das medidas.É preciso indicar com clareza se a estimativa utilizada é a mesma para os diferentes cenários e diferentes valores da utilização. **A determinação da fase transiente deve ser independente da semente inicial. Comprove isso no relatório.**

### 4. Tabelas com os resultados e comentários pertinentes (35 pontos)

Comente os resultados obtidos. Procure analisar a evolução dos valores e o porquê de sua obtenção. Garanta que todos os resultados analíticos estão dentro do intervalo de confiança. Isso é essencial! Apresente os resultados analíticos conhecidos junto com os valores medidos.

Para cada utilização indique precisamente o número de rodadas, o tamanho das rodadas (explique como foi determinado), e o tamanho da fase transiente. 

### 5. Otimização (15 pontos)

Para cada valor de utilização, obtenha os resultados otimizados, isto é, considerando sempre o número de eventos de partida computados, procure determinar FATOR MÍNIMO (disciplina) = número de rodadas x tamanho de rodada (número de partidas) + fases transientes (número de partidas desprezadas), que satisfaz no seu simulador aos requisitos do tamanho do intervalo de simulação, independente do valor de utilização. Este fator mínimo deve ser independente da semente e isso tem que ser demonstrado. Ao escolher nova semente, garanta que os resultados ótimos continuam a ser válidos. Documente isso.

Obviamente, este FATOR será obtido para a métrica mais crítica, entre parâmetro e valor de utilização. Com seu simulador operando corretamente, a busca da combinação ótima dará um bônus extra ao grupo que conseguir os menores valores, dentro de uma margem de 20%. Se por exemplo, um grupo conseguir 1.000.000 eventos de partida como FATOR MÍNIMO e outro tenha conseguido 1.200.000, eles estarão tecnicamente empatados e ambos ganharão bônus (20% a mais na nota). 

Como a simulação é muito simples, o maior interesse é na otimização. Procure demonstrar que você conseguiu de fato o menor tamanho de rodada e o menor número de rodadas para cada valor de utilização. Mostre que você encontrou o mínimo solicitado com algum recurso gráfico. Busque o ponto ótimo de forma automática sempre que possível. Tudo deve ser documentado. 

### 6. Conclusões (10 pontos)

Coloque aqui seus comentários finais.

Descreva dificuldades encontradas, as otimizações feitas, e outras conclusões que você tirou do trabalho. Indique o tempo que foi gasto para executar todas as rodadas necessárias para a simulação dos resultados, bem como informações da máquina usada (processador, memória, etc). Comente o que poderia ser melhorado, como, por exemplo, o tempo de execução do seu programa, caso haja soluções nitidamente mais eficientes. Adicione quaisquer comentários que você julgar relevante.

Cada uma das seções terá sua avaliação. Portanto, não deixe de colocar nenhuma seção no seu relatório. Não deixe de ler o capítulo de simulação na apostila.

### 7. Anexo - Listagem documentada do programa (10 pontos)

A documentação do programa fonte deverá ser feita com rigor, explicando cada sub-rotina ou passo da programação. Código fonte sem comentários não é aceitável. Mande a listagem do código fonte como um anexo ao relatório. 

O Grupo deve apresentar um executável funcionando na apresentação do trabalho,  em PC Windows ou Linux Ubuntu, ou em máquina própria. O executável deve ser passível de ser rodado com uma escolha arbitrária do número de fregueses por rodada e número de rodadas. 

O relatório completo deve ser entregue impresso (e não em mídia eletrônica). 

Uma versão eletrônica do documento impresso deve ser disponibilizada, adicionalmente. O programa executável deverá ser enviado para aguiar@nce.ufrj.br. 

Se o Grupo usar alguma linguagem específica, ele deve compilar o ambiente e apresentar um executável que rode sem necessidade de instalação especial, em Windows 10 ou Ubuntu. O programa será testado com alguns valores particulares para averiguar sua correção e integridade.
