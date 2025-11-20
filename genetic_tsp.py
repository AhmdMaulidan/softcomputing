import random

def solve_tsp(dist_matrix, pop_size, generations, tournament_k, pc, pm, elite_size):
    """
    Solves the Traveling Salesperson Problem using a Genetic Algorithm.

    Args:
        dist_matrix (list of lists): The distance matrix between cities.
        pop_size (int): The size of the population.
        generations (int): The number of generations to run.
        tournament_k (int): The number of individuals in a tournament selection.
        pc (float): The crossover probability.
        pm (float): The mutation probability.
        elite_size (int): The number of elite individuals to carry over.

    Returns:
        dict: A dictionary containing the best route, its distance, and history.
    """
    num_cities = len(dist_matrix)

    def route_distance(route):
        """Calculates the total distance of a given route."""
        total_dist = 0
        for i in range(num_cities):
            # Get the distance from the current city to the next one in the route
            from_city = route[i]
            # The next city, wrapping around from the last to the first
            to_city = route[(i + 1) % num_cities]
            total_dist += dist_matrix[from_city][to_city]
        return total_dist

    def create_individual():
        """Creates a random individual (a permutation of cities)."""
        ind = list(range(num_cities))
        random.shuffle(ind)
        return ind

    def initial_population():
        """Creates the initial population."""
        return [create_individual() for _ in range(pop_size)]

    def tournament_selection(pop):
        """Selects an individual using tournament selection."""
        tournament = random.sample(pop, tournament_k)
        # Return the best individual from the tournament
        return min(tournament, key=route_distance)

    def ordered_crossover(p1, p2):
        """Performs ordered crossover (OX1) between two parents."""
        a, b = sorted(random.sample(range(num_cities), 2))
        child = [-1] * num_cities
        
        # Copy the slice from the first parent
        child[a:b + 1] = p1[a:b + 1]
        
        # Fill the rest with genes from the second parent
        p2_idx = 0
        for i in range(num_cities):
            if child[i] == -1:
                while p2[p2_idx] in child:
                    p2_idx += 1
                child[i] = p2[p2_idx]
        return child

    def swap_mutation(ind):
        """Performs swap mutation on an individual."""
        a, b = random.sample(range(num_cities), 2)
        ind[a], ind[b] = ind[b], ind[a]
        return ind

    # --- Main GA Loop ---
    pop = initial_population()
    best_overall_ind = min(pop, key=route_distance)
    best_overall_dist = route_distance(best_overall_ind)
    history = []

    for _ in range(generations):
        # Sort population by fitness (lower distance is better)
        pop = sorted(pop, key=route_distance)
        
        # Get the best individual of the current generation
        best_current_ind = pop[0]
        best_current_dist = route_distance(best_current_ind)
        
        # Update the overall best if the current best is better
        if best_current_dist < best_overall_dist:
            best_overall_ind = best_current_ind
            best_overall_dist = best_current_dist

        # --- FIXED: Record the best of the CURRENT generation for the graph ---
        history.append(best_current_dist)

        # Create the next generation
        new_pop = pop[:elite_size] # Carry over the elite

        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop)
            p2 = tournament_selection(pop)
            
            child = ordered_crossover(p1, p2) if random.random() < pc else p1[:]
            
            if random.random() < pm:
                child = swap_mutation(child)
                
            new_pop.append(child)
        
        pop = new_pop

    return {
        "best_route": best_overall_ind,
        "best_distance": best_overall_dist,
        "history": history
    }
