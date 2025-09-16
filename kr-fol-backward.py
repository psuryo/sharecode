# First-Order Logic Knowledge Representation with Backward Chaining

class KnowledgeBase:
    def __init__(self):
        self.facts = {}
        self.rules = []

    def add_fact(self, predicate, arguments):
        """Add a fact to the knowledge base."""
        if predicate not in self.facts:
            self.facts[predicate] = set()
        self.facts[predicate].add(tuple(arguments))

    def add_rule(self, condition, conclusion):
        """Add a rule to the knowledge base (condition -> conclusion)."""
        self.rules.append((condition, conclusion))

    def backward_chain(self, predicate, arguments, bindings=None, visited=None):
        """Perform backward chaining to prove a query (predicate, arguments)."""
        if bindings is None:
            bindings = {}
        if visited is None:
            visited = set()

        # Substitute arguments with current bindings
        query_args = tuple(bindings.get(arg, arg) for arg in arguments)
        goal = (predicate, query_args)
        
        # Check if the goal is a fact
        if predicate in self.facts and query_args in self.facts[predicate]:
            return [bindings]
        
        # Check for circular reasoning
        if goal in visited:
            return []
        visited.add(goal)

        # Try to prove the goal using rules
        solutions = []
        for condition, conclusion in self.rules:
            conc_pred, conc_args = conclusion
            
            # Check if the rule's conclusion matches the query's predicate and arity
            if conc_pred == predicate and len(conc_args) == len(arguments):
                # Unify the conclusion with the query
                new_bindings = bindings.copy()
                match = True
                for conc_arg, query_arg in zip(conc_args, arguments):
                    if isinstance(conc_arg, str) and conc_arg.islower():  # It's a variable
                        if conc_arg in new_bindings:
                            if new_bindings[conc_arg] != query_arg:
                                match = False; break
                        else:
                            new_bindings[conc_arg] = query_arg
                    elif conc_arg != query_arg:  # It's a constant
                        match = False; break
                
                if match:
                    # Recursively prove the conditions
                    proofs = self._prove_conditions(condition, new_bindings, visited.copy())
                    solutions.extend(proofs)
        return solutions

    def _prove_conditions(self, conditions, bindings, visited):
        """Helper to prove a list of conditions recursively."""
        if not conditions:
            return [bindings]
        
        cond_pred, cond_args = conditions[0]
        remaining_conditions = conditions[1:]

        solutions = []
        if cond_pred in self.facts:
            for fact_args in self.facts[cond_pred]:
                # Try to unify the condition with the fact
                current_bindings = bindings.copy()
                match = True
                
                # Unify variables in condition with constants in fact
                for cond_arg, fact_arg in zip(cond_args, fact_args):
                    if isinstance(cond_arg, str) and cond_arg.islower():
                        if cond_arg in current_bindings:
                            if current_bindings[cond_arg] != fact_arg:
                                match = False; break
                        else:
                            current_bindings[cond_arg] = fact_arg
                    elif cond_arg != fact_arg:
                        match = False; break
                
                if match:
                    # Recursively try to prove the next condition with the new bindings
                    proofs = self._prove_conditions(remaining_conditions, current_bindings, visited)
                    solutions.extend(proofs)
        return solutions

    def query(self, predicate, arguments):
        """Query the knowledge base to check if a predicate with given arguments is true."""
        return len(self.backward_chain(predicate, arguments)) > 0

# Example usage
def main():
    kb = KnowledgeBase()

    kb.add_fact("Parent", ["john", "mary"])
    kb.add_fact("Parent", ["mary", "alice"])
    kb.add_fact("Parent", ["john", "bob"])
    kb.add_fact("Male", ["john"])
    kb.add_fact("Female", ["mary"])
    kb.add_fact("Female", ["alice"])

    kb.add_rule([("Parent", ["x", "y"]), ("Parent", ["y", "z"])], ("Grandparent", ["x", "z"]))
    kb.add_rule([("Parent", ["x", "y"]), ("Male", ["x"])], ("Father", ["x", "y"]))
    kb.add_rule([("Parent", ["x", "y"]), ("Female", ["x"])], ("Mother", ["x", "y"]))

    print("First-Order Logic with Backward Chaining Example")
    print("-----------------------------------------------")

    print(f"Is John a father of Mary? {kb.query('Father', ['john', 'mary'])}")
    print(f"Is Mary a mother of Alice? {kb.query('Mother', ['mary', 'alice'])}")
    print(f"Is John a grandparent of Alice? {kb.query('Grandparent', ['john', 'alice'])}")
    print(f"Is John a grandparent of Mary? {kb.query('Grandparent', ['john', 'mary'])}")
    print(f"Is Alice a father of Bob? {kb.query('Father', ['alice', 'bob'])}")
    print(f"Is Bob a parent of John? {kb.query('Parent', ['bob', 'john'])}")

if __name__ == "__main__":
    main()
