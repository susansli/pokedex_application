# Pokédex Application

An executable developed with Python and Python GUI tool Tkinter which lets you search up Pokémon info. 

Uses data from PokéAPI and Smogon Usage Stats API to show both game-relevant as well as Smogon's competitive information for the Gen 8 OU tier.

I always find myself scrolling through Bulbapedia and Smogon endlessly whenever I play games like Pokémon Reborn (sorry, but I can't keep track of 800+ Pokémon), so I thought about building something like this, which will hopefully not only help me but anyone else who doesn't want to spend all that time searching.

### Installation

Simply boot up pokedex_application_launcher.exe! Do not delete the icon or background files please.

I've also included the working Python file in the python_file directory.

### Endpoints

1) PokeAPI: https://pokeapi.co/

This API is where game relevant information such as name, type, base stats, and images are obtained from.

2) Smogon Usage Stats API: https://smogon-usage-stats.herokuapp.com/

This API was used to obtain stats for Gen 8 OU recommendations (that is, the most common setups) for relevant Pokémon. Pokémon that are NFE (with some exceptions), not in the tier, or are not used enough with relevant data will not have this information available.

### Assets

The Pokéball graphic used in the icon and background are free use from Freepik.

### Future Plans

- Include informaiton (perhaps map graphics) of encounter areas in main game series
- Include Pokémon Reborn specific information

### Notes

- There are some sprites with minor graphical issues (such as a white background), but this is very minor; similarly, some sprites may be missing front or back views.
- In order to search up Pokémon with different forms, enter it in name-form format, eg. Aegislash-blade.
- Some missing entries or incorrect data for Sword and Shield Pokémon.
- The initial (and only the initial) fetch may be slower than normal, please be a little patient
