import os
import csv
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

BATCH_SIZE = 500


# ---------------------------
# Neo4j connection
# ---------------------------
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# ---------------------------
# RESET DATABASE
# ---------------------------
def reset_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")


# ---------------------------
# CREATE NODE BATCH
# ---------------------------
def create_nodes(tx, nodes):
    query = """
    UNWIND $nodes AS node
    MERGE (n:User {id: node.id})
    SET n.name = node.name,
        n.group = node.group
    """
    tx.run(query, nodes=nodes)


# ---------------------------
# CREATE EDGE BATCH
# ---------------------------
def create_edges(tx, edges):
    query = """
    UNWIND $edges AS edge
    MATCH (a:User {id: edge.from})
    MATCH (b:User {id: edge.to})
    MERGE (a)-[:FOLLOWS]->(b)
    """
    tx.run(query, edges=edges)


# ---------------------------
# STREAM CSV GENERATOR
# ---------------------------
def lines(file_path):
    with open(file_path, newline="", encoding="utf-8") as f:
        for row in f:
            if len(row) > 0 and not row.startswith("//"):
                yield row

def stream_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(lines(file_path))
        for row in reader:
            yield row


# ---------------------------
# BULK IMPORT HELPER
# ---------------------------
def batch_import(session, generator, batch_size, writer_fn):
    batch = []

    for item in generator:
        batch.append(item)

        if len(batch) >= batch_size:
            session.execute_write(writer_fn, batch)
            print(f"Inserted batch of {len(batch)}")
            batch = []

    if batch:
        session.execute_write(writer_fn, batch)
        print(f"Inserted final batch of {len(batch)}")


# ---------------------------
# MAIN
# ---------------------------
def main():
    nodes_file = "data/nodes.csv"
    edges_file = "data/edges.csv"

    with driver.session() as session:

        # 1. RESET DATABASE
        print("Resetting graph...")
        session.execute_write(reset_graph)

        # 2. IMPORT NODES
        print("Importing nodes...")
        node_gen = stream_csv(nodes_file)
        batch_import(session, node_gen, BATCH_SIZE, create_nodes)

        # 3. IMPORT EDGES
        print("Importing edges...")
        edge_gen = stream_csv(edges_file)
        batch_import(session, edge_gen, BATCH_SIZE, create_edges)

    print("Import completed.")


if __name__ == "__main__":
    main()