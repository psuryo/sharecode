# First-Order Logic Knowledge Representation with Backward Chaining

class KnowledgeBase:
    def __init__(self):
        # Facts: Dictionary mapping predicates to sets of tuples (e.g., {"Parent": {("john", "mary"), ("mary", "alice")}})
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

    def backward_chain(self, predicate, arguments, visited=None):
        """Perform backward chaining to prove a query (predicate, arguments)."""
        if visited is None:
            visited = set()  # Track visited goals to avoid infinite recursion

        goal = (predicate, tuple(arguments))
        if goal in visited:
            return False  # Avoid infinite recursion
        visited.add(goal)

        # Check if the fact exists directly
        if predicate in self.facts and tuple(arguments) in self.facts[predicate]:
            return True

        # Try to prove the goal using rules
        for condition, conclusion in self.rules:
            conc_pred, conc_args = conclusion
            if conc_pred != predicate or len(conc_args) != len(arguments):
                continue

            # Check if conclusion matches the query (simple unification)
            bindings = {}
            match = True
            for c_arg, q_arg in zip(conc_args, arguments):
                if c_arg.startswith("x"):  # Variable in rule
                    bindings[c_arg] = q_arg
                elif c_arg != q_arg:  # Constants must match
                    match = False
                    break
            if not match:
                continue

            # Check if all conditions of the rule can be proven
            all_conditions_true = True
            for cond_pred, cond_args in condition:
                # Substitute variables in condition arguments
                new_args = []
                for arg in cond_args:
                    if arg in bindings:
                        new_args.append(bindings[arg])
                    else:
                        new_args.append(arg)
                # Recursively prove the condition
                if not self.backward_chain(cond_pred, new_args, visited.copy()):
                    all_conditions_true = False
                    break

            if all_conditions_true:
                return True

        return False

    def query(self, predicate, arguments):
        """Query the knowledge base to check if a predicate with given arguments is true."""
        return self.backward_chain(predicate, arguments)

# Example usage
def main():
    # Initialize knowledge base
    kb = KnowledgeBase()

    # Add facts
    kb.add_fact("Parent", ["john", "mary"])
    kb.add_fact("Parent", ["mary", "alice"])
    kb.add_fact("Parent", ["john", "bob"])
    kb.add_fact("Male", ["john"])
    kb.add_fact("Female", ["mary"])
    kb.add_fact("Female", ["alice"])

    # Add rules
    # Rule 1: Parent(x, y) ^ Parent(y, z) -> Grandparent(x, z)
    kb.add_rule([("Parent", ["x", "y"]), ("Parent", ["y", "z"])], ("Grandparent", ["x", "z"]))
    # Rule 2: Parent(x, y) ^ Male(x) -> Father(x, y)
    kb.add_rule([("Parent", ["x", "y"]), ("Male", ["x"])], ("Father", ["x", "y"]))
    # Rule 3: Parent(x, y) ^ Female(x) -> Mother(x, y)
    kb.add_rule([("Parent", ["x", "y"]), ("Female", ["x"])], ("Mother", ["x", "y"]))

    print("First-Order Logic with Backward Chaining Example")
    print("-----------------------------------------------")

    # Perform queries
    print(f"Is John a father of Mary? {kb.query('Father', ['john', 'mary'])}")
    print(f"Is Mary a mother of Alice? {kb.query('Mother', ['mary', 'alice'])}")
    print(f"Is John a grandparent of Alice? {kb.query('Grandparent', ['john', 'alice'])}")
    print(f"Is Mary a grandparent of Alice? {kb.query('Grandparent', ['mary', 'alice'])}")
    print(f"Is Alice a father of Bob? {kb.query('Father', ['alice', 'bob'])}")
    print(f"Is Bob a parent of John? {kb.query('Parent', ['bob', 'john'])}")

if __name__ == "__main__":
    main()
