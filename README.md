# Special Queries

Dieses Projekt demonstriert die besonderen Stärken von Graphdatenbanken anhand eines synthetischen Beispielgraphen.

Der Fokus liegt auf Graphalgorithmen und Fragestellungen, die in relationalen Datenbanken nur sehr schwer oder ineffizient umsetzbar sind.

## Ziel des Projekts

Eine Graphdatenbank unterscheidet sich von klassischen Datenbanken nicht nur durch ihre Datenstruktur, sondern vor allem durch die Art der möglichen Fragestellungen.

Dieses Projekt zeigt:

- wie Netzwerke modelliert werden
- wie Graphalgorithmen angewendet werden
- welche Analysen nur in Graphdatenbanken effizient möglich sind
- wie strukturelle Eigenschaften eines Netzwerks sichtbar werden

## Datengrundlage

Der Graph besteht aus:

- 32 Knoten (User)
- 59 Kanten (FOLLOWS-Beziehungen)

## Import-Hinweise

Vor dem Import muss einiges beachtet werden.

### `.env` Datei anlegen

Im Projektverzeichnis muss eine `.env` Datei erstellt werden, die die Verbindung zur Neo4j-Instanz definiert:

```
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

Ohne diese Datei kann das Import-Script keine Verbindung zur Datenbank herstellen.

### Bestehende Daten werden gelöscht

Beim Import wird die Datenbank komplett zurückgesetzt:

```cypher
MATCH (n)
DETACH DELETE n
```

Das bedeutet:

- alle Knoten werden gelöscht
- alle Beziehungen werden gelöscht
- der Graph wird vollständig neu aufgebaut

### Backup

Falls sich bereits wichtige Daten in der Neo4j-Instanz befinden, sollte vorher ein Export erstellt werden:

- Neo4j Browser Export-Funktion verwenden
- oder neo4j-admin dump nutzen
- oder relevante Queries als CSV sichern

## Importieren der Daten

Die Daten werden über ein Python-Script in Neo4j importiert:

```bash
uv run python src/main.py
```

## Setup-Schritte

1. Start der Neo4j Instanz
1. Reset und Import des Beispielgraphen
1. Validierung der Daten

## Validierung der Datenbank

Nach dem Import können folgende Queries zur Überprüfung verwendet werden:

Anzahl der Knoten (32 erwartet):

```cypher
MATCH (n)
RETURN count(n);
```

Anzahl der Kanten (59 erwartet):

```cypher
MATCH ()-[r]->()
RETURN count(r);
```

## Aufgabenstellung

Unter „Fragestellungen“ findest du mehrere thematisch sortierte Graphanalyse-Kategorien.

Vorgehensweise:

1. Bearbeite zuerst „Kürzeste Wege“
   - führe die gegebenen Queries aus
   - interpretiere die Ergebnisse
1. Bearbeite anschließend „Erreichbarkeit“
   - ergänze fehlende Queries selbstständig
   - committe deine Lösungen ins Repository
1. Entwickle für alle weiteren Themen passende Fragestellungen
   - nutze die bisherigen Beispiele als Vorlage
   - arbeite ggf. mit KI-Unterstützung
   - dokumentiere jede Fragestellung im gleichen Format: Fragestellung + passende Cypher Query

## Fragestellungen

### Kürzeste Wege (Shortest Path)

➡ mehr dazu [hier](./queries/01.ShortestPath.md)

Analyse von:

- minimalen Verbindungen zwischen Knoten
- Informationsfluss im Netzwerk
- Distanz zwischen Communities

### Erreichbarkeit (Reachability)

➡ mehr dazu [hier](./queries/02.Reachability.md)

Analyse von:

- ob Knoten überhaupt miteinander verbunden sind
- Netzwerkzugänglichkeit
- strukturelle Isolation von Gruppen

### Connected Components

Analyse von:

- zusammenhängenden Teilgraphen
- isolierten Netzwerken
- globaler Netzwerkstruktur

### Zentralitätsmaße

Analyse von:

- wichtigen Knoten im Netzwerk
- Einfluss und Vermittlung

Metriken:

- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- Eigenvector Centrality

### PageRank

Analyse von:

- „Wichtigkeit“ basierend auf Struktur
- Einfluss durch eingehende Verbindungen
- iterative Netzwerkbewertung

### Community Detection

Analyse von:

- automatisch erkannten Gruppen
- Cluster-Strukturen im Netzwerk
- Dichte vs. schwache Verbindungen

### Ähnlichkeitsmaße

Analyse von:

- strukturell ähnlichen Knoten
- gemeinsamen Nachbarschaften

Methoden:

- Jaccard Similarity
- Common Neighbors
- Adamic-Adar (optional)

### Link Prediction

Analyse von:

- wahrscheinlich neuen Verbindungen
- fehlenden Kanten im Netzwerk
- Struktur-basierter Vorhersage

### Maximum Flow / Minimum Cut

Analyse von:

- Engpässen im Netzwerk
- maximalem Informationsfluss
- kritischen Verbindungen

### Graph Embeddings

Analyse von:

- Vektor-Repräsentationen von Knoten
- maschinellem Lernen auf Graphen
- Node2Vec / DeepWalk Konzepten

## Lernziel

Nach Bearbeitung dieses Projekts sollen folgende Fähigkeiten aufgebaut werden:

- Verständnis von Graphdatenmodellen
- Anwendung von Cypher Queries
- Interpretation von Netzwerkstrukturen
- Verständnis zentraler Graphalgorithmen
- Einordnung von Graphproblemen vs. SQL-Problemen
