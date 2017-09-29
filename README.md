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

### 2. Teste de Correção (10 pontos)

### 3. Estimativa de fase transiente (10 pontos)

### 4. Tabelas com os resultados e comentários pertinentes (35 pontos)

### 5. Otimização (15 pontos)

### 6. Conclusões (10 pontos)

### 7. Anexo - Listagem documentada do programa (10 pontos)

