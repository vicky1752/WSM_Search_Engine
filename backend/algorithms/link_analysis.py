
def pagerank(graph, iterations=20, damping=0.85):

    nodes = list(graph.keys())
    total = len(nodes)

    if total == 0:
        return {}

    rank = {node: 1 / total for node in nodes}

    for _ in range(iterations):

        new_rank = {}

        for node in nodes:

            score = (1 - damping) / total

            for source in nodes:

                links = graph[source]

                if node in links and len(links) > 0:
                    score += (
                        damping * rank[source] / len(links)
                    )

            new_rank[node] = score

        rank = new_rank

    return rank


def hits(graph, iterations=20):

    nodes = list(graph.keys())

    authority = {node: 1.0 for node in nodes}
    hub = {node: 1.0 for node in nodes}

    for _ in range(iterations):

        new_authority = {
            node: sum(
                hub[source]
                for source in nodes
                if node in graph[source]
            )
            for node in nodes
        }

        new_hub = {
            node: sum(
                new_authority[target]
                for target in graph[node]
            )
            for node in nodes
        }

        authority_norm = sum(v*v for v in new_authority.values()) ** 0.5
        hub_norm = sum(v*v for v in new_hub.values()) ** 0.5

        if authority_norm:
            authority = {
                k: v / authority_norm
                for k, v in new_authority.items()
            }

        if hub_norm:
            hub = {
                k: v / hub_norm
                for k, v in new_hub.items()
            }

    return authority, hub

