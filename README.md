# Model that were used: NEAT
NEAT, which stands for NeuroEvolution of Augmenting Topologies, is a popular algorithm in the field of artificial intelligence, specifically in the domain of evolutionary computation and neuroevolution. It was introduced by Kenneth O. Stanley and Risto Miikkulainen in 2002.

NEAT is designed to evolve artificial neural networks (ANNs) with the goal of solving complex tasks or problems. Unlike traditional neural network training methods that rely on gradient-based optimization algorithms, NEAT employs an evolutionary approach inspired by natural selection.

## Some key features and concepts associated with NEAT:

Genetic Encoding: NEAT uses a genetic encoding scheme to represent neural networks. Each neural network is encoded as a genome, which includes information about the structure of the network, such as nodes and connections.

Complexification through Evolution: NEAT evolves populations of neural networks over generations. During evolution, it allows for the addition of new nodes and connections to the neural network architecture, enabling the algorithm to explore more complex structures over time.

Innovation and Speciation: NEAT introduces a mechanism for tracking innovation in the evolving population. It encourages diversity by maintaining separate species of neural networks. This helps prevent premature convergence and allows for the exploration of different solutions.

Fitness Evaluation: The performance of each neural network is measured using a fitness function that evaluates how well the network performs the given task. The fitness scores guide the evolutionary process, influencing the selection of individuals for reproduction.

Crossover and Mutation: NEAT employs genetic operators like crossover and mutation to create offspring. Crossover involves combining the genomes of two parent networks to produce a child, while mutation introduces small changes to the genomes.

Historical Marking: To track innovations across generations, NEAT uses historical marking. Each gene in the genome is assigned a historical marker, allowing the algorithm to identify whether a gene represents a new or an existing connection.

Adaptive Evolution: NEAT allows for the adaptive evolution of neural network structures. As the population evolves, the algorithm can discover and retain neural network architectures that prove to be more effective in solving the given problem.

NEAT has been applied to various tasks, including game playing, robotics, and optimization problems. Its ability to dynamically evolve neural network structures has made it a popular choice for researchers interested in evolving complex, adaptive systems.
