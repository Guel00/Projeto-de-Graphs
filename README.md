# Prática 1 — Grafos: Roteamento e Coloração em Redes

Solução para os dois problemas clássicos de grafos aplicados a infraestrutura de redes:

- **Parte 1** — Caminho de menor custo em rede de backbone (Dijkstra / Bellman-Ford)
- **Parte 2** — Alocação de canais Wi-Fi sem interferência (Coloração com DSatur)

---

## Estrutura do repositório

```
projeto/
├── backend/
│   ├── roteamento_coloração_redes.py            # Algoritmos de roteamento
│   └── alocacao_canais_wifi.py                  # Algoritmo de coloração
│── README.md
└── main.py          # Interface gráfica (Tkinter)
```

---

## Requisitos

- Python **3.8 ou superior**
- Sem dependências externas — apenas bibliotecas da instalação padrão do Python

Verifique sua versão com:

```bash
python --version
```

---

## Como rodar

### Interface gráfica (recomendado)

```bash
python main.py
```

A janela abre com duas abas — uma para cada parte. Em cada aba:

1. Clique em **Carregar arquivo** e selecione o `.txt` correspondente
2. O conteúdo do arquivo aparece na prévia
3. Clique em **Resolver**
4. O resultado aparece na caixa verde

> O algoritmo da Parte 1 é escolhido automaticamente: **Dijkstra** se não houver pesos negativos, **Bellman-Ford** se houver.

---

### Linha de comando (alternativo)

Você também pode rodar cada parte diretamente pelo terminal, sem a interface:

**Parte 1 — Roteamento:**

```bash
cd backend
python roteamento_coloração_redes.py <arquivo_entrada> <arquivo_saida>

# Exemplos:
python roteamento_coloração_redes.py grafo_rede_p.txt saida_rot_p.txt
python roteamento_coloração_redes.py grafo_rede_m.txt saida_rot_m.txt
```

**Parte 2 — Coloração:**

```bash
cd backend
python alocacao_canais_wifi.py <arquivo_entrada> <arquivo_saida>

# Exemplos:
python alocacao_canais_wifi.py grafo_wifi_p.txt saida_aloc_p.txt
python alocacao_canais_wifi.py grafo_wifi_m.txt saida_aloc_m.txt
```

---

## Formato dos arquivos de entrada

**Parte 1** (`grafo_rede_*.txt`) — separador TAB:

```
<num_vertices>	<num_arestas>
<S>	<T>
<u>	<v>	<custo>
...
```

**Parte 2** (`grafo_wifi_*.txt`) — separador TAB:

```
<num_vertices>	<num_arestas>
<u>	<v>
...
```

---

## Formato das saídas geradas

**Parte 1:**

```
ALGORITMO: Dijkstra
JUSTIFICATIVA: Todos os pesos são não-negativos, portanto Dijkstra é aplicável...
ROTA: 0 2 3 4
CUSTO: 11
```

**Parte 2:**

```
ALGORITMO: DSatur
JUSTIFICATIVA: DSatur ordena vértices pelo grau de saturação...
NUM_CORES: 3
COLORACAO: 0=1 1=2 2=3 3=1 4=2
```

---

## Algoritmos utilizados

### Parte 1 — Roteamento

| Grafo              | Algoritmo    |                   Justificativa                         |
|--------------------|--------------|---------------------------------------------------------|
| `grafo_rede_p.txt` | Dijkstra     | Sem pesos negativos; O((V+E) log V) com heap            |
| `grafo_rede_m.txt` | Bellman-Ford | Pesos negativos (SLA); O(V·E); detecta ciclos negativos |

### Parte 2 — Coloração

| Algoritmo | Complexidade | Garante ótimo    |
|-----------|--------------|------------------|
| DSatur    |   O(V²)      | Quase sempre sim |

