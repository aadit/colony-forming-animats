
Colony Formation
CS263C Final Project Report

Lawrence Chang

Aadit Patel

UCLA Fall 2013


I. Hypothesis

The main hypothesis of this project is to induce colony formation in insect-like animats through learning, which in turn will minimize collective energy expenditure as a secondary effect. The animats’ environment contains multiple food sources that each animat must eat in order to survive. Animats are able to sense food gradients, eat food, and pickup or drop food. Colonies should form in between food source locations, such that animats will not need to unnecessarily expend energy  traversing the map to eat multiple foods. Effectively placed colonies should include animats that return to food sources to bring food back to the colony.

II.  Issues/Problems

We had two main issues while developing the animat/environment system:

1. Gradient Sensing
In order to successfully form colonies, the animats must have already evolved to successfully follow food gradients when hungry. We initially modeled our animats’ brain by using a neural net with the PyBrain library. To simulate an evolved ability of gradient sensing, we utilized a supervised learning session before running our experiments in which the animat would be exposed to correct examples of gradient following. However, even after a thorough amount of training sets, the animat was still unlikely to accurately follow food gradients. The ultimate solution to this issue was to use a Q-Learner agent and remove the neural network.

2. Animat Survival
We modeled each animat to require a specific amount each food energy to survive. However, this constraint proved too harsh for the animats. Before animats could learn to form colonies, they would lose their energy and die. Tweaking maximum and starting energy levels only allowed the animats to survive longer before eventually dying out. Ultimately, we decided to disable death in animats and just allow a fixed number of animats to learn in the environment.

III. Methodology

The project focused on simplifying the physics of the system (environment and animats) by abstracting unnecessary complexities. Each time step, an animat is able to perform a single action of out seven possible actions:
Move North
Move East
Move South
Move West
Eat Food
Pickup Food
Drop Food

The project did not concentrate on colony formation through communication. Colony formation should occur through a combination of environmental factors and learning. The environmental factors we are interested in varying through experiments are:
Spatial food distribution
Food density (how many bites a food lasts for)
Food regeneration rate
Energy costs/rewards for movement, living, multiple food consumption

Furthermore, we constrained our system with the following abstractions:
There are no collisions. Animats can walk through and stand on top of other animats or food items. A location on the map that stacks multiple types of food sources and multiple animats is considered a colony.
Multiple foods can share the same physical location. An animat can only interact with food (eat/pickup) if it is directly on top of it.
Movement and direction are restricted to strictly vertical and horizontal directions.
Animats can sense each food type. Food smells follow an inverse square law. The agent also receives a small reward when successfully following a food gradient. This abstracts out the initial evolved brain of the animat.

IV.  Instrumentation

We collected the following data for each of our experiments: 

Energy level of each food source for each animat
Number of times each animat ate multiple food types in a tick 
Number of times each animat dropped a food of one type onto a food of another type
Net energy change per tick (over the entire animat population)
Number of multiple food types eaten in a single tick (over the entire animat population)

We also captured  a visual animation for each experiment to see where colonies were forming spatially in the environment.

V. Environment, Physics, and Food Types

Spatial Grid
The animat environment had the following properties:
2.5D rectangular grid
Hard boundaries at the edges of the rectangular grid
Only horizontal and vertical movements allowed.
Manhattan distances between points
Each distinct food type is represented by an Environment object and gradient map. 
The gradient maps follow an inverse square law. 
Gradients are additive, such that two foods on top of each other will double all gradient values produced by those foods.

Food 
Food objects have the following properties:
Each food belongs to one of four distinct food types.
Foods have a bite count. The bite count of a food is decremented each time an animat eats that food. 
When the bite count reaches zero, the food is removed from the environment.
Food can be picked up or dropped by an animat.
Food cannot be eaten if it is being held by an animat. However, it can still be sensed by other animats while being held.

Food Generators
Food generator objects produce food at a specific location at a specified rate. A natural analogue to food generators may be a fruit tree or a lake teeming with fish. A food generator can only produce one distinct type of food, which is specified when creating the generator.

VI. Animat 

Body
The animat agent has an effector that can pick up or drop a food item at a time. It also contains distinct energy stores and energy usage rates for each type of food it can eat.

Brain Attempt 1: PyBrain Neural Network
We used the PyBrain Neural Network package to initially model our animat brain. The input neurons were the values of the North, West, South, East, and Current directions, relative to the animat, and the output layer was the direction the animat should move in. We generated training samples and performed supervised learning with three different methods :

We generated gradient values between 0 and 1 from a uniform distribution for each direction, determined the direction of the maximum gradient, and set that direction to the output direction.
We generated gradient values between 0 and 1 from a triangular distribution (biased towards 1) to better simulate actual gradient values in the environment.
We collected actual gradient values by sampling the gradient map.

All three of these sampling and training methods resulted in subpar gradient sensing. The animat would often get stuck, move randomly, or “ping-pong” between two food sources. This would not induce colony formation.

Brain Attempt 2: State Machine
The second attempt at the brain structure was to use a state machine that would hard-code interactions between the animats and their environment. The state machine was able to move the animat in the direction of the food gradient without error. The goal was to add additional functionality and states that would enable basic colony forming actions.

For example:
Go to Food 1 and pick it up.
Go towards Food 2.
Drop Food 1.
Simultaneously eat both Food 1 and Food 2, receiving an increased energy bonus.

Such a hard coded approach did not offer aspects of adaptation, learning, or evolution. We considered using a probabilistic approach to the state machine, where different actions weren’t determined completely by the present state, but rather with a random exploration element. 

Brain Attempt 3: Q-Learner
Our last brain implementation was a Q-Learner. We explored using a neural network to hold Q-values (continuous state space), but settled on using finite set of state and actions in a Q-Table to reduce complexity.

The state of an animat is represented by:
Target Food - the food gradient the animat should be following. This is the food corresponding to the energy store that the animat is lowest on. An animat cannot target a food type if it is currently holding that a food of that type (2 bits).
Holding Food - if an animat is holding a food item of a certain type (4 bits, one for each food type).
On Food - if an animat is currently on a food of a certain type (4 bits, one for each food type)
Gradient - for each food type, which direction (North, South, East, West) is the highest gradient value  (8 bits, 2 for each food type).

The possible actions the Q-Learner can take from any given state are:
Move North
Move South
Move East
Move West
Eat Food
Pickup Food
Drop Food

The total state space is 2^18 states, and the total action space is 7 actions.
Reward Function and Animat Energy Gains/Costs
Each iteration, the animat assesses its current state, chooses and performs an action, and enters a new state. The action performed determines a reward via the reward function. The reward function is based on the net change in energy between the current and next states, and have the following properties:
Apply a cost of living every iteration.
If the animat has moved from the current state to the next state, apply cost of movement.
There is no cost for picking up/dropping food.
There is no cost for eating when there is no food present.
There is a small reward for correctly moving towards the target food. The reward offsets the living and movement costs.
The sum of the energy cost is distributed over all energy stores, according to the energy usage rates. For example, if the total energy cost is 4 units, and the animat has an energy usage rate of [0.5, 0.25, 0.125, 0.125] for the 4 energy types, the energy cost to each energy type would be [2, 1, 0.5, 0.5], respectively.
When an animat eats food, add the food energy amount to the respective energy 
If an animat eats multiple food sources in an iteration, add an exponential energy to each energy source for each multiple food source eaten.
The reward is the net energy change, summed over each energy source.


VII. Algorithms / System Architecture

The overall system is based on a global time tick.

During each global tick:
Each environments tick. Environments handle food locations, food generation, and food states.
Each animat ticks. An animat’s tick involve:
Get current animat state
Get target food source type, and direction
Use Q-table and current state, receive action to take
A chosen action is performed
Food objects are manipulated based on action
Calculate a reward based on result of action and environment
Get new state (after action)
Use the previous state, current state, action taken, and reward received, to update the Q table. This is the Q learning.
Depending on desired length, data and a snapshot of the system is captured, which is animated at the end to visually inspect animat movements, colonies,  etc.


VIII.  Experiments

1. Two food types, two food generators, two opposite corners
Two food generators, of different food types, were placed at opposite corners of the map. 
Hypothesis - a colony forms between the two food sources.
Result - Colonies were formed at various points in the map, not necessarily directly between the two food sources. However, due to the Manhattan distances between the corners, any point along the diagonal connecting the unoccupied corners was equidistant to the food sources. Therefore, any point along this diagonal could be considered “between” the two food sources. Colonies were formed at such locations.

2. Four food types, four food generators, between corners
From a corner, traveling to an adjacent corner is equidistant to traveling to the middle. To incentivize colony formation in the middle of the map, we placed food sources not in the corners, but between them. This made it so traveling between foods was less efficient than traveling to the center of the map.
Hypothesis - the colonies form in the middle of the map
Result - Colonies formed close to the center between the four food sources (see video).
Result - There was a steady increase in the number of times multiple foods were eaten after initial colony formation. See Figure 2-1.
Video: http://www.youtube.com/watch?v=z23c7ERFXh8



















Figure 2-1

3. Allow Q state table to have a “desire”, based on which energy level (corresponding to a specific food source) was lowest.
A two-bit state was added to encode a value between 0 and 3, to represent each of the four food types. Hard coded logic determines which food should be “targeted”, based on the specific energy level and usage rate.
Hypothesis - the animats continue to form colonies between all four food sources, but have a better balance of energy levels at the end of the run.
Results were unexpected. Colonies formed less frequently, sometimes none at all. Instead, each animat was more likely to go directly to the food source that it “targeted”. Visually, the animats were seen traversing the map between various food source points. 

4. Four food types, four food items, infinite bite count, placed between corners
Hypothesis - Because there were only four food items, and they were of infinite size, given enough time the animats would drag the four food items to one location, and reap the benefits.
After 30,000 iterations, the four food items were brought close together, sometimes very close. However, there was never an instance where all four food items were put on the same spot (x-y coordinate), and all four consumed at once. 
This result appears to be because of the inherent stochasticity in the animats’ behavior. While there is a bias to bring foods closer together to reduce movement energy expenditure, there is no direct logic that causes animats to place foods on top of one another, then never move them. There is always some level of randomness that some animat will move food away from an ideal pile.
Net energy of animats rose over time, as a result of less distances traveled between foods. See Figure 4-1 below.
Over time, the animats consume multiple foods per bite at a faster rate. See Figure 4-2 below.
Video: http://www.youtube.com/watch?v=A5l0J79_6KY




Figure 4-1

Figure 4-2
5. Allow death
Until this point, death was not an element in our system. Introduce this element to see how well the animats can survive.
Hypothesis - some animats adapt quickly enough to survive, while others do not and die off.
Results were unexpected. Instead of some animats learning to survive while others dying off, it was an all or nothing affair. Given various values of maximum energy level, starting energy level, energy usage rate, movement energy usage, etc, either all animats in our system die or all survive. Data gathered included the dead or alive status of animats.
It is not unreasonable to think that enough finessing of these parameters would result in an ideal distribution of survivors and non-survivors. However, introducing such adaptation through evolution/mutation/reproduction does not seem helpful in reaching our hypothesis. Rather, we can create generations, where after a given set of time, the animats who performed “best” would be selected and allowed to reproduce for a subsequent generation.
6. Distributed colony formation
Place food generators in such a manner as to induce multiple colony locations.
Food generators for types 2, 3, and 4 are placed at the top of the map, as well as bottom.
A single food generator for type 1 is placed in the middle of the map.
Hypothesis - two colonies would form, in the two regions sandwiched by all four food types.
Result - There was no consistent colony. Colonies were often found at food generator locations, an unsurprising result. One issue may again deal with Manhattan distances. Although foods 2, 3, and 4 were meant to be equidistant to the lone food 1, food 3 was actually closer. Also, distances between the top and bottom of map were equal to distance to center, resulting in smaller colonies forming along the left and right edges.
Possible next steps
Place the foods in a less linear fashion
Introduce diagonal movements
Vary bite sizes, food generation rates
Video: http://www.youtube.com/watch?v=MAjXl7vl8Zg

IX.  Current Status of Work

Working
Each of our runs involves an initial training session.
A training session consists of:
100x100 environment
20 animats, randomly distributed, with uninitialized Q tables
Variable amounts of food. Each food type is present. Randomly distributed.
Animats explore the environment, receiving positive and negative rewards for their actions.
After training, we run an experiment. The same functionality can be eventually used to support generational evolution.

Not Yet Implemented/ To do
Introduce death. Offspring will be either a clone or combination of parents. Those that survive longer and gain enough energy will produce offspring. Selectional pressure gives rise to more intelligent and better adapted animats.
The introduction of death requires balancing several parameters:
Maximum energy pool size
Starting energy amount
Living cost
Movement cost
Energy gain from eating 1, 2, 3, or 4 foods
Number of food generators
Food generation frequency
Food bite size
Generational evolution. After a certain number of time steps, manually pick out the best animats. Start a new experiment / session with these animats, perhaps duplicated to the same population number as before. “Best” will be subjective, using the statistics we’ve identified as critical and beneficial to survival and colony formation.
Adaptations to vary dependence on different food types. At present, all food types are required equally, and their respective energy pools are drained equally. A feature that could produce interesting results is allowing these values to vary through mutation. The food type requirements would be normalized, so that you can’t have a zero requirement for all foods. If one food requirement goes down, another food’s must go up.

Given enough barriers between locations, such as distance or semipermeable walls, adaptations can lead to speciation depending on a local environment. Animats in an environment with only food sources 1 and 2 may evolve to only depend on those, and not require food sources 3 and 4.
Realism to foods
Variable bite sizes
Food degradation over time: loses bite size, eventually disappears.
Animat carrying the food can eat it. Presently, a food item that is held cannot be eaten by anyone.
Costs to carry food
		Would colonies form even if there was a direct negative reward for carrying food?

X.  Two Person Team -- Contributions

The extended code repository can be found on GitHub: 
https://github.com/aadit/colony-forming-animats

Lawrence
Environment mechanics
Food source mechanics
State machine
Q learner
Q learner states
Animations
Animat mechanics
Experiments

Aadit
Project idea/proposal
Hypothesis
Experiments
Animat mechanics
Neural net using PyBrain
Q learner reward function
Animat energy gains/expenditures
Statistics/Data collection

XI.  Languages, Tools, Packages

The code was written exclusively in Python. We chose Python because classmates were using Python, and exploring the PyBrain package.

Several Python packages proved useful, including:
numpy, for creating and manipulating matrices.The environment/food maps were two dimensional matrices, holding various food gradient values to be accessed by the animats
http://www.numpy.org
matplotlib, for providing display and animation capability to show our animats and foods
http://matplotlib.org
Studywolf, a blog that discusses Q-learning and provided example code
http://studywolf.wordpress.com/2012/11/25/reinforcement-learning-q-learning-and-exploration/
PyBrain, for our initial attempt at the brain using neural nets
http://pybrain.org





