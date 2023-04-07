# Greeblies V1
A little simulation game to see the relationships of different one cell organisms and how they interact. 

***************************************
***  Jean-Louis Marin 2023 - April. ***
***************************************

***************************************
Single Cell Simulation - Greeblies 
Version 1.0
***************************************

This program simulates the behavior of a single cell organism.
Greens photoplancton organisms are the primary producers of the ecosystem. They don't die of starvation, they have constant light, but they can be eaten by predators. 
Browns are the primary consumers of the ecosystem. They eat greens and die of starvation. And are the primary food source for omnivores.
Yellows are the secondary consumers of the ecosystem. They eat greens and browns and die of starvation. And are the primary food source for carnivores.
Reds are the tertiary consumers of the ecosystem. They eat yellows and die of starvation.

The variables to adjust are the number of organisms, the speed of the organisms, and the light intensity, and starvation counter.
The organisms are randomly placed on the screen and move randomly.
The organisms are drawn on the screen and the number of organisms of each type is displayed. -- BROKEN --
The organisms are stored in a database. not ready yet. the information is dumped but needs ferter refinement.

To Do:
******
1. Add a GUI to adjust the number of organisms, the speed of the organisms, and the light intensity.
2. Add a GUI to display the number of organisms of each type.
3. create a record of each even for each organism in the simulation in the database.
4. Hook up the database to BI reporting dashboard. for stats at the of the simulation.
5. create various hooks in the code to link exteral ML or AI to evolve the organisms' behavior each generation of the game.
6. Move the simulation to cloud hosted server with a web front end.
7. Add a GUI to adjust the number of organisms, the speed of the organisms, and the light intensity.
8. increase the model to gargantuan proportions for the simulation. for multiple people to interact with. 

** - baseline code established = April 7th 2023. 

'''
