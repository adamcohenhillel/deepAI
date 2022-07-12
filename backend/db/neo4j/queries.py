"""ORM-like approach to neo4j nodes
"""

def find_matches(tx, number_of_relations):
    query = """
    MATCH (d1:DeepRequest)-->(a:AdjectiveNode)<--(d2:DeepRequest)
    WITH d1, d2, collect(a) as related_adjectives
    WHERE size(related_adjectives) > $number_of_related
    RETURN d1, d2, related_adjectives
    """
    result = tx.run(query, number_of_relations=number_of_relations)
    record = result.single()
    return record["node_id"]
