import sys


def dsatur(n, adj):

    color = [0] * n                          
    saturation = [0] * n                    
    neighbor_colors = [set() for _ in range(n)]
    degree = [len(adj[v]) for v in range(n)]

    for _ in range(n):
        u = max(
            (v for v in range(n) if color[v] == 0),
            key=lambda v: (saturation[v], degree[v]),
        )
        
        used = neighbor_colors[u]
        c = 1
        while c in used:
            c += 1

        color[u] = c

        for w in adj[u]:
            if c not in neighbor_colors[w]:
                neighbor_colors[w].add(c)
                saturation[w] += 1

    return color


def validate_coloring(n, adj, color):
    for u in range(n):
        for v in adj[u]:
            if color[u] == color[v]:
                return False, (u, v)
    return True, None


def solve_from_text(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    n, _ = map(int, lines[0].split("\t"))
    adj = [[] for _ in range(n)]

    for line in lines[1:]:
        parts = line.split("\t")
        u, v = int(parts[0]), int(parts[1])
        adj[u].append(v)
        adj[v].append(u)

    color = dsatur(n, adj)

    valid, conflict = validate_coloring(n, adj, color)
    if not valid:
        raise RuntimeError(f"Coloracao invalida: vertices {conflict[0]} e {conflict[1]} tem mesma cor.")

    num_colors = max(color)
    coloring_str = " ".join(f"{v}={color[v]}" for v in range(n))

    justificativa = (
        "DSatur ordena vertices pelo grau de saturacao (numero de cores distintas "
        "nos vizinhos), priorizando os mais restritos a cada passo. "
        "Isso tende a produzir coloracoes muito próximas ao otimo x(G) "
        "sem a complexidade exponencial do backtracking exato."
    )

    output = (
        f"ALGORITMO: DSatur\n"
        f"JUSTIFICATIVA: {justificativa}\n"
        f"NUM_CORES: {num_colors}\n"
        f"COLORACAO: {coloring_str}\n"
    )
    return output


def solve(input_path, output_path):
    with open(input_path, "r") as f:
        content = f.read()
    output = solve_from_text(content)

    with open(output_path, "w") as f:
        f.write(output)

    print(output)
    print(f"Saída salva em: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python parte2.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)
    solve(sys.argv[1], sys.argv[2])
