# Simple Knowledge Representation using a Semantic Network

# Knowledge base: dictionaries to represent "is-a" and "has-property" relationships
knowledge_base = {
    "is_a": {
        "cat": "mammal",
        "dog": "mammal",
        "mammal": "animal",
        "sparrow": "bird",
        "bird": "animal"
    },
    "has_property": {
        "cat": ["whiskers", "fur"],
        "dog": ["fur", "barks"],
        "sparrow": ["feathers", "flies"],
        "mammal": ["warm_blooded"],
        "bird": ["warm_blooded", "lays_eggs"]
    }
}

def is_a(entity, category):
    """Check if an entity belongs to a category (directly or indirectly)."""
    current = entity
    while current in knowledge_base["is_a"]:
        if knowledge_base["is_a"][current] == category:
            return True
        current = knowledge_base["is_a"][current]
    return False

def has_property(entity, property_name):
    """Check if an entity has a specific property (directly or inherited)."""
    # Check direct properties
    if entity in knowledge_base["has_property"] and property_name in knowledge_base["has_property"][entity]:
        return True
    # Check inherited properties
    current = entity
    while current in knowledge_base["is_a"]:
        parent = knowledge_base["is_a"][current]
        if parent in knowledge_base["has_property"] and property_name in knowledge_base["has_property"][parent]:
            return True
        current = parent
    return False

def get_all_properties(entity):
    """Retrieve all properties of an entity, including inherited ones."""
    properties = set()
    # Add direct properties
    if entity in knowledge_base["has_property"]:
        properties.update(knowledge_base["has_property"][entity])
    # Add inherited properties
    current = entity
    while current in knowledge_base["is_a"]:
        parent = knowledge_base["is_a"][current]
        if parent in knowledge_base["has_property"]:
            properties.update(knowledge_base["has_property"][parent])
        current = parent
    return list(properties)

# Example usage
def main():
    print("Knowledge Representation Example")
    print("-----------------------------")
    
    # Query: Is a cat an animal?
    print(f"Is a cat an animal? {is_a('cat', 'animal')}")
    
    # Query: Does a dog have fur?
    print(f"Does a dog have fur? {has_property('dog', 'fur')}")
    
    # Query: Does a sparrow have fur?
    print(f"Does a sparrow have fur? {has_property('sparrow', 'fur')}")
    
    # Query: What properties does a cat have?
    print(f"Properties of a cat: {get_all_properties('cat')}")
    
    # Query: What properties does a sparrow have?
    print(f"Properties of a sparrow: {get_all_properties('sparrow')}")

if __name__ == "__main__":
    main()
