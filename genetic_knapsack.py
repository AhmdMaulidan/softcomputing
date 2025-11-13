import random

# --- Konfigurasi Dasar ---
# Anda dapat menyesuaikan nilai-nilai ini untuk mengubah cara kerja algoritma
POPULATION_SIZE = 50       # Jumlah individu (solusi) dalam satu populasi
MAX_GENERATIONS = 100      # Jumlah generasi maksimum yang akan dijalankan
MUTATION_RATE = 0.05       # Peluang terjadinya mutasi pada sebuah gen
ELITISM_COUNT = 2          # Jumlah individu terbaik yang langsung dibawa ke generasi berikutnya

class Item:
    """Mewakili satu item yang bisa dimasukkan ke dalam knapsack."""
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

    def __repr__(self):
        return f"Item(N: {self.name}, W: {self.weight}, V: {self.value})"

def calculate_fitness(chromosome, items, max_weight):
    """
    Menghitung nilai 'fitness' dari sebuah kromosom (solusi).
    Fitness diukur dari total nilai item, tetapi menjadi 0 jika total berat melebihi kapasitas.
    """
    total_weight = 0
    total_value = 0
    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_weight += items[i].weight
            total_value += items[i].value
    
    # Penalti: Jika berat melebihi kapasitas, solusi tidak valid (fitness = 0)
    if total_weight > max_weight:
        return 0
    return total_value

def create_initial_population(items_count):
    """Menciptakan populasi awal secara acak."""
    population = []
    for _ in range(POPULATION_SIZE):
        chromosome = [random.randint(0, 1) for _ in range(items_count)]
        population.append(chromosome)
    return population

def selection(population, items, max_weight):
    """
    Memilih dua 'parent' dari populasi menggunakan metode 'tournament selection'.
    Individu dengan fitness lebih tinggi lebih mungkin terpilih.
    """
    # Ambil 5 kandidat acak dari populasi untuk turnamen
    tournament_entrants = random.sample(population, 5)
    
    # Urutkan kandidat berdasarkan fitness-nya (tertinggi ke terendah)
    fittest_entrant = max(
        tournament_entrants, 
        key=lambda chrom: calculate_fitness(chrom, items, max_weight)
    )
    return fittest_entrant

def crossover(parent1, parent2):
    """
    Menghasilkan dua 'child' baru dengan menggabungkan gen dari dua 'parent'.
    Menggunakan 'single-point crossover'.
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(chromosome):
    """
    Mengubah gen secara acak (0 menjadi 1 atau 1 menjadi 0) berdasarkan MUTATION_RATE.
    Ini membantu menjaga keragaman genetik.
    """
    mutated_chromosome = []
    for gene in chromosome:
        if random.random() < MUTATION_RATE:
            mutated_chromosome.append(1 - gene) # Flip the bit
        else:
            mutated_chromosome.append(gene)
    return mutated_chromosome

def solve(items, max_weight):
    """
    Fungsi utama yang menjalankan seluruh proses algoritma genetika.
    """
    items_count = len(items)
    population = create_initial_population(items_count)
    
    best_solution_ever = None
    best_fitness_ever = -1
    
    # Log untuk melacak progres setiap generasi
    generation_log = []

    for generation in range(MAX_GENERATIONS):
        # Hitung fitness untuk setiap individu di populasi saat ini
        fitness_scores = [calculate_fitness(chrom, items, max_weight) for chrom in population]
        
        # Simpan individu terbaik dari generasi saat ini
        current_best_fitness = max(fitness_scores)
        current_best_idx = fitness_scores.index(current_best_fitness)
        current_best_chromosome = population[current_best_idx]
        
        if current_best_fitness > best_fitness_ever:
            best_fitness_ever = current_best_fitness
            best_solution_ever = current_best_chromosome

        # Catat data generasi ini
        generation_log.append({
            "generation": generation + 1,
            "best_fitness": current_best_fitness,
            "average_fitness": sum(fitness_scores) / len(fitness_scores)
        })

        # --- Proses Evolusi ---
        next_generation = []
        
        # 1. Elitisme: Bawa individu terbaik langsung ke generasi berikutnya
        sorted_population = sorted(population, key=lambda c: calculate_fitness(c, items, max_weight), reverse=True)
        elites = sorted_population[:ELITISM_COUNT]
        next_generation.extend(elites)
        
        # 2. Crossover & Mutasi: Buat sisa populasi baru
        while len(next_generation) < POPULATION_SIZE:
            parent1 = selection(population, items, max_weight)
            parent2 = selection(population, items, max_weight)
            
            child1, child2 = crossover(parent1, parent2)
            
            mutated_child1 = mutate(child1)
            mutated_child2 = mutate(child2)
            
            next_generation.append(mutated_child1)
            if len(next_generation) < POPULATION_SIZE:
                next_generation.append(mutated_child2)

        population = next_generation

    # Siapkan hasil akhir
    final_selected_items = [items[i] for i, gene in enumerate(best_solution_ever) if gene == 1]
    final_total_weight = sum(item.weight for item in final_selected_items)
    final_total_value = sum(item.value for item in final_selected_items)

    result = {
        "best_solution_chromosome": best_solution_ever,
        "selected_items": final_selected_items,
        "total_weight": final_total_weight,
        "total_value": final_total_value,
        "generation_log": generation_log
    }

    return result
