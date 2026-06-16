import sys
import heapq


def bellman_ford(n, edges, src, dst):
    INF = float("inf")
    dist = [INF] * n
    prev = [-1] * n
    dist[src] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    # Verificação de ciclo negativo
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise ValueError("Ciclo negativo detectado no grafo.")

    if dist[dst] == INF:
        raise ValueError(f"Sem caminho de {src} até {dst}.")

    path = []
    at = dst
    while at != -1:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path, dist[dst]


def dijkstra(n, adj, src, dst):
    INF = float("inf")
    dist = [INF] * n
    prev = [-1] * n
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    if dist[dst] == INF:
        raise ValueError(f"Sem caminho de {src} até {dst}.")

    path = []
    at = dst
    while at != -1:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path, dist[dst]


def format_cost(cost):
    if isinstance(cost, float) and cost == int(cost):
        return str(int(cost))
    return str(cost)


def solve(input_path, output_path):
    with open(input_path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    n, _ = map(int, lines[0].split("\t"))
    src, dst = map(int, lines[1].split("\t"))

    edges = []
    has_negative = False
    for line in lines[2:]:
        parts = line.split("\t")
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        edges.append((u, v, w))
        if w < 0:
            has_negative = True

    if has_negative:
        algo = "Bellman-Ford"
        justificativa = (
            "O grafo contem arestas com peso negativo (acordos SLA), "
            "o que invalida o uso de Dijkstra. "
            "Bellman-Ford suporta pesos negativos e detecta ciclos negativos, "
            "sendo a escolha correta para este cenario."
        )
        path, cost = bellman_ford(n, edges, src, dst)
    else:
        algo = "Dijkstra"
        justificativa = (
            "Todos os pesos são nao-negativos, portanto Dijkstra e aplicavel "
            "e mais eficiente que Bellman-Ford neste caso, "
            "com complexidade O((V+E) log V) usando fila de prioridade."
        )
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
        path, cost = dijkstra(n, adj, src, dst)

    output = (
        f"ALGORITMO: {algo}\n"
        f"JUSTIFICATIVA: {justificativa}\n"
        f"ROTA: {' '.join(map(str, path))}\n"
        f"CUSTO: {format_cost(cost)}\n"
    )

    with open(output_path, "w") as f:
        f.write(output)

    print(output)
    print(f"Saída salva em: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python parte1.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)
    solve(sys.argv[1], sys.argv[2])
