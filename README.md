# Greeblies V1
A little simulation game to visualise the relationships of different one cell organisms and how they interact. 

![Greeblies!](images/Greeblies_Title.png)

***************************************
***  Jean-Louis Marin 2023 - April. ***
***************************************

***************************************
Single Cell Simulation - Greeblies 
Version 1.0
***************************************

This program simulates the behavior of a single cell organism.
Greens phytoplankton organisms are the primary producers of the ecosystem. They don't die of starvation, they have constant light, but they can be eaten by predators. 
Browns are the primary consumers of the ecosystem. They eat greens and die of starvation. And are the primary food source for omnivores.
Yellows are the secondary consumers of the ecosystem. They eat greens and browns and die of starvation. And are the primary food source for carnivores.
Reds are the tertiary consumers of the ecosystem. They eat yellows and die of starvation.

The variables to adjust are the number of organisms, the speed of the organisms, and the light intensity, and starvation counter.
The organisms are randomly placed on the screen and move randomly.
The organisms are drawn on the screen and the number of organisms of each type is displayed. -- BROKEN --
The organisms are stored in a database. not ready yet. the information is dumped but needs further refinement.

To Do:
******
1. Add a GUI to adjust the number of organisms, the speed of the organisms, and the light intensity.
2. Add GAME OVER dialog with reason code. 
3. Create a record of each even for each organism in the simulation in the database. - commented out for now
4. Hook up the database to BI reporting dashboard. for stats at the of the simulation. - commented out for now
5. Create various hooks in the code to link external ML or AI to evolve the organisms' behavior each generation of the game.
6. Move the simulation to cloud hosted server with a web front end.
7. Increase the model to gargantuan proportions for the simulation. for multiple people to interact with. 

******
V1.23-4
Displays the individual numbers of organisms of each type.

** - baseline code established = April 7th 2023. 

'''
