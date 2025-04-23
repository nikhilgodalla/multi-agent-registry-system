# Validation and Test Procedures for Multi AI Agents Infrastructure

## Database Cleanup

Before starting validation, clear all nodes and relationships in Neo4j:

```cypher
MATCH (n)
DETACH DELETE n;
```

## Test Sequences

### Test Sequence 1: New Agent Creation

```
# First Request - Should create a new agent
{
    "parent_id": "parent_A",
    "problem_statement": "Create a data analysis report for Q1 2024 sales performance"
}
```

### Test Sequence 2: Similar Problem (Should Reuse Agent)

```
# Second Request - Similar problem, should reuse the first agent
{
    "parent_id": "parent_B",
    "problem_statement": "Analyze Q1 2024 sales performance and create report"
}
```

### Test Sequence 3: Different Domain - New Agent

```
{
  "parent_id": "parent_data_1",
  "problem_statement": "Analyze customer behavior patterns in e-commerce data"
}
```

### Test Sequence 4: Similar Domain (Reuse Agent from Test 3)

```
{
  "parent_id": "parent_data_2",
  "problem_statement": "Study e-commerce customer behavior and shopping patterns"
}
```

### ChromaDB Verification

Run the script `list_chroma.py` to verify stored agents in ChromaDB.

## Neo4j Verification Queries

Run these queries in Neo4j browser:

```cypher
// Query 1: View all nodes and relationships
MATCH (p)-[r:DEPENDS_ON]->(c)
RETURN p, r, c;

// Query 2: Count unique agents
MATCH (a:Agent)
RETURN count(a) as AgentCount;

// Query 3: Count relationships
MATCH ()-[r:DEPENDS_ON]->()
RETURN count(r) as RelationshipCount;

// Query 4: View all DummyAgent nodes
MATCH (d:DummyAgent)
RETURN d;
```

## Expected Results

- **Test 1:** New agent created.
  - Message: "New agent created and mapped"
- **Test 2:** Reuse agent from Test 1.
  - Message: "Existing agent found and mapped"
- **Test 3:** New agent created (different domain).
  - Message: "New agent created and mapped"
- **Test 4:** Reuse agent from Test 3.
  - Message: "Existing agent found and mapped"

## Neo4j Expected State

- Exactly 2 unique Agent nodes
- 4 DummyAgent nodes (parent_A through parent_D)
- 4 DEPENDS_ON relationships
- No duplicate relationships

## Additional Edge Case Tests

### Test 1 (No agents exist, null parent_id):

```json
{
  "parent_id": null,
  "problem_statement": "Initial system setup and configuration"
}
```
- **Expected:** Creates super parent node and maps the agent.

### Test 2 (Agents exist, invalid null parent_id):

```json
{
  "parent_id": "",
  "problem_statement": "Update system configuration settings"
}
```
- **Expected:** Rejects request with 400 error.

### Test 3 (Valid parent_id provided):

```json
{
  "parent_id": "super_parent_abcd1234",
  "problem_statement": "Implement feature X for the platform"
}
```
- **Expected:** Processes normally and maps agent under specified parent.

