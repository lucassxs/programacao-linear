#  Otimização Linear



### Tratamento do módulo

Vamos tratar o módulo para obter um problema de otimização linear. Introduzimos novas variáveis ai^+ e ai^- não negativas e ai = ai^+ - ai^-. E a restrição Ax = b se transforma em Ax^+ - Ax^- = b.

Já construímos o problema com essas duas variáveis desde o início. No final utilizamos a função findAccelerations() para obter as acelerações.

### Discretização

Vamos aproximar o valor das integrais através de retângulos de base time_increment. Logo time_increment será o intervalo de discretização e a entrada do programa.

A função objetivo agora é uma somatória de acelerações multiplicadas pela base time_increment. Ao todo serão 10/time_increment retângulos na discretização da integral.

```python
  # Constructing the coefficients vector of the objective function
  c = []
  for i in range(2*n):
      c.append(time_increment)
```

As integrais das restrições também foram discretizadas de acordo com a função objetivo. A velocidade no instante t é o somatório das acelerações até o instante t multiplicadas por time_increment e posição no instante t é o somatório das velocidades até o instante t.

Fiz as contas com time_increment = 2 e as restrições ficam da seguinte forma:

`v(0) = a(0) = 0
v(2) = a(0) + a(2)
v(4) = a(0) + a(2) + a(4)
v(6) = a(0) + a(2) + a(4) + a(6)
v(8) = a(0) + a(2) + a(4) + a(6) + a(8)
v(10) = a(0) + a(2) + a(4) + a(6) + a(8) + a(10) = 0
`

`x(0) = v(0) = 0
x(2) = v(0) + v(2)
x(4) = v(0) + v(2) + v(4)
x(6) = v(0) + v(2) + v(4) + v(6)
x(8) = v(0) + v(2) + v(4) + v(6) + v(8)
x(10) = v(0) + v(2) + v(4) + v(6) + v(8) + v(10) = 1
`

Obtemos:

`x(0)= v(0) = 0
1) v(10) = a(0) + a(2) + a(4) + a(6) + a(8) + a(10) = 0
2) x(10) = v(0) + v(2) + v(4) + v(6) + v(8) + v(10) = 1
`

Substituindo as velocidades encontradas antes em 2), obtemos:

`2) x(10) = 5*a(2) + 4*a(4) + 3*a(6) + 2*a(8) + a(10) = 1`

Assim temos duas restrições, uma de velocidade e a outra de posição.
Generalizando, as expressões e substituindo pelas variáveis novas da discretização:


```python

# Constructing the equality constraints matrix
  A_eq = [[], []]
  b_eq = [1, 0]

  # Constructing the position constraint
  for i in range(0, 2*n, 2):
      ai = (10/time_increment + 1) - (i+1)/2
      A_eq[0].append(ai)
      A_eq[0].append(-ai)

  # Constructing the velocity constraint
  for i in range(0, 2*n, 2):
      A_eq[1].append(1)
      A_eq[1].append(-1)
```

### Método Simplex

Esta implementação do método simplex recebe o problema na forma canônica onde todas as restrições são de igualdade e as variáveis são todas não-negativas.
A versão do Simplex implementada utiliza o método Big M.

### Resultados

Foi testado com dois intervalos de discretização diferentes:

Com time_increment = 1, obtemos:

![](/imgs/ac1.png)

![](/imgs/vel1.png)

![](/imgs/pos1.png)

Com time_increment = 0.2

![](/imgs/ac3.png)

![](/imgs/vel2.png)

![](/imgs/pos2.png)

Agora aqui observa-se o consumo do foguete (custo final) variando conforme o intervalo de discretização é dividido por 2. Nota-se que o gráfico se assemelha a uma função exponencial.

![](/imgs/cost.png)
