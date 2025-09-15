# First-Order Logic Knowledge Representation Example

# Knowledge base consists of facts and rules
class KnowledgeBase:
    def __init__(self):
        # Facts: Dictionary mapping predicates to sets of tuples (e.g., {"Mammal": {("cat",), ("dog",)}})
        self.facts = {}
        # Rules: List of (condition, conclusion) where condition is a list of predicates, conclusion is a predicate
        self.rules = []

    def add_fact(self, predicate, arguments):
        """Add a fact to the knowledge base."""
        if predicate not in self.facts:
            self.facts[predicate] = set()
        self.facts[predicate].add(tuple(arguments))

    def add_rule(self, condition, conclusion):
        """Add a rule to the knowledge base (condition -> conclusion)."""
        self.rules.append((condition, conclusion))

    def forward_chain(self):
        """Apply forward chaining to infer new facts."""
        new_facts_added = True
        while new_facts_added:
            new_facts_added = False
            for condition, conclusion in self.rules:
                # Check if all predicates in the condition are satisfied
                if all(pred in self.facts and tuple(args) in self.facts[pred] for pred, args in condition):
                    # Add the conclusion as a new fact
                    predicate, args = conclusion
                    if predicate not in self.facts:
                        self.facts[predicate] = set()
                    if tuple(args) not in self.facts[predicate]:
                        self.facts[predicate].add(tuple(args))
                        new_facts_added = True

    def query(self, predicate, arguments):
        """Check if a predicate with given arguments is true."""
        self.forward_chain()  # Ensure all inferences are made
        return predicate in self.facts and tuple(arguments) in self.facts[predicate]

# Example usage
def main():
    # Initialize knowledge base
    kb = KnowledgeBase()

    # Add facts
    kb.add_fact("Mammal", ["cat"])
    kb.add_fact("Mammal", ["dog"])
    kb.add_fact("Bird", ["sparrow"])

    # Add rules
    # Rule 1: Mammal(x) -> Animal(x)
    kb.add_rule([("Mammal", ["x"])], ("Animal", ["x"]))
    # Rule 2: Bird(x) -> Animal(x)
    kb.add_rule([("Bird", ["x"])], ("Animal", ["x"]))
    # Rule 3: Mammal(x) -> HasFur(x)
    kb.add_rule([("Mammal", ["x"])], ("HasFur", ["x"]))
    # Rule 4: Bird(x) -> CanFly(x)
    kb.add_rule([("Bird", ["x"])], ("CanFly", ["x"]))

    print("First-Order Logic Knowledge Base Example")
    print("--------------------------------------")

    # Perform queries
    print(f"Is a cat an animal? {kb.query('Animal', ['cat'])}")
    print(f"Is a dog an animal? {kb.query('Animal', ['dog'])}")
    print(f"Is a sparrow an animal? {kb.query('Animal', ['sparrow'])}")
    print(f"Does a cat have fur? {kb.query('HasFur', ['cat'])}")
    print(f"Can a sparrow fly? {kb.query('CanFly', ['sparrow'])}")
    print(f"Does a dog have fur? {kb.query('HasFur', ['dog'])}")
    print(f"Can a cat fly? {kb.query('CanFly', ['cat'])}")

    # Print all inferred facts
    print("\nAll Inferred Facts:")
    for predicate, args_set in kb.facts.items():
        for args in args_set:
            print(f"{predicate}{args}")

if __name__ == "__main__":
    main()
