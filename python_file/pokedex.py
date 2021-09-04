import tkinter as tk
import requests
import urllib.request
from PIL import Image, ImageTk
import io


def HEIGHT() -> int:
    """Return the height of the application.

    :return: the height of the application window
    """
    return 600


def WIDTH() -> int:
    """Return the width of the application.

    :return: the width of the application window
    """
    return 800


def IMG_HEIGHT() -> int:
    """Return the height of the Pokemon image.

    :return: the height of the Pokemon image
    """
    return 250


def IMG_WIDTH() -> int:
    """Return the width of the Pokemon image.

    :return: the with of the Pokemon image
    """
    return 250


def FRAME_COLOR() -> str:
    """Return the hex color of the application's frames.

    :return: hex of frame color
    """
    return "#59BFFF"


def BUTTON_COLOR() -> str:
    """Return the hex color of the search button.

    :return: hex of search button color
    """
    return "#006EE6"


def FONT() -> str:
    """Return the font family and size of the application.

    :return: application's font and size
    """
    return "Helvetica 11"


def populate_dex(name: str):
    """Populate the application with data.

    :param name: a string or or a positive integer
    :precondition: name argument is a string or a positive integer
    :precondition: results will only be displayed if there is a valid response from the initial API call
    :postcondition: populates application with correct info if entry exists in API, else display that the query yielded
    no results
    """
    url = "https://pokeapi.co/api/v2/pokemon/" + name
    res = requests.get(url)
    if not res:
        no_results()
    else:
        pokemon = res.json()
        dex_res(pokemon)
        display_images(pokemon)
        try:
            get_smogon_info(name)
        except KeyError:
            smogon_info["text"] = "GEN 8 COMPETITIVE SMOGON OU SETS\n\nThis Pokémon is not part of the Gen 8 OU tier."


def dex_res(pokemon: dict):
    """Get Pokedex data and populate dex info label.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key ["forms"][i]["name"] where i is a positive integer
    and the value is a string
    :precondition: pokemon must be a dictionary containing the key ["id"] where the value is a positive integer
    :precondition: all the conditions for the function pokemon_type to work correctly are met
    :precondition: all the conditions for the function ability to work correctly are met
    :precondition: all the conditions for the function base_stats to work correctly are met
    :precondition: a tkinter label exists called "dex_info"
    :postcondition: populates the dex_info label with a formatted string with correct values
    """
    name = pokemon["forms"][0]["name"].capitalize()
    pokemon_id = pokemon["id"]
    types = pokemon_type(pokemon)
    abilities = ability(pokemon)
    stats = base_stats(pokemon)
    formatted_str = "\nName: %s \n\nDex Number: %s\n\nType(s): %s \n\nAbilities: %s \n\nBase Stats:\n %s" % \
                    (name, pokemon_id, types, abilities, stats)
    dex_info["text"] = formatted_str


def display_images(pokemon: dict):
    """Get image and sprite data and populate image and sprite labels.

    :param pokemon: a dictionary
    :precondition: all the conditions for the function get_image to work correctly are met
    :precondition: all the conditions for the function get_sprite to work correctly are met
    :postcondition: populate image and sprite labels with correct images if they exist, else display nothing
    """
    try:
        get_image(pokemon["sprites"]["other"]["official-artwork"]["front_default"])
    except AttributeError:
        dex_img.configure(image=None)
        dex_img.image = None
    try:
        get_sprite(pokemon["sprites"]["front_default"], "front")
    except AttributeError:
        sprite_front_img.configure(image=None)
        sprite_front_img.image = None
    try:
        get_sprite(pokemon["sprites"]["back_default"], "back")
    except AttributeError:
        sprite_back_img.configure(image=None)
        sprite_back_img.image = None


def ability(pokemon: dict) -> str:
    """Get the Pokemon's abilities from PokeAPI.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key pokemon["abilities"][i]["ability"]["name"] where
    i is a positive integer and the value is a string
    :postcondition: gets and formats the names of the Pokemon's abilities
    :return: a formatted string representing the Pokemon's abilities
    """
    abilities_list = []
    for i in range(len(pokemon["abilities"])):
        abilities_list.extend([pokemon["abilities"][i]["ability"]["name"].capitalize(), ", "])
    return ''.join(abilities_list)[:-2]


def base_stats(pokemon: dict) -> str:
    """Get the Pokemon's base stats from PokeAPI.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key pokemon["stats"][i]["stat"]["name"] where i is a
    positive integer and the value is a string
    :precondition: pokemon must be a dictionary containing the key pokemon["stats"][i]["base_stat"] where i is a
    positive integer and the value is a positive integer
    :postcondition: gets and formats the names of the Pokemon's base stats
    :return: a formatted string representing the Pokemon's base stats
    """
    base_stat_list = []
    for i in range(len(pokemon["stats"])):
        base_stat_list.extend([pokemon["stats"][i]["stat"]["name"].capitalize() + " : " +
                               str(pokemon["stats"][i]["base_stat"]), '\n'])
    return ''.join(base_stat_list)


def pokemon_type(pokemon: dict) -> str:
    """Get the Pokemon's types from PokeAPI.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key pokemon["types"][i]["type"]["name"] where i is a
    positive integer and the value is a string
    :postcondition: gets and formats the names of the Pokemon's types
    :return: a formatted string representing the Pokemon's types
    """
    types_list = []
    for i in range(len(pokemon["types"])):
        types_list.extend([pokemon["types"][i]["type"]["name"].capitalize(), ", "])
    return ''.join(types_list)[:-2]


def get_image(url: str):
    """Get the Pokemon's image from PokeAPI and display it in the image frame.

    This function uses urllib to get the image data from the given url, creates a resized raw image, and then passes
    it to Tkinter.
    :param url: a string
    :precondition: tkinter label dex_img must exist
    :precondition: the constants IMG_HEIGHT and IMG_WIDTH must exist and be positive integers
    :postcondition: converts image data from link into a resized image compatible with ImageTk
    :postcondition: configures the dex_img label to display image from url
    """
    with urllib.request.urlopen(url) as data:
        image_data = data.read()
    raw_image = Image.open(io.BytesIO(image_data))
    resize_image = raw_image.resize((IMG_HEIGHT(), IMG_WIDTH()), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(resize_image)
    dex_img.configure(image=image)
    dex_img.image = image


def get_sprite(url: str, face: str):
    """Get the Pokemon's sprites from PokeAPI and display it in the sprites frames.

    This function uses urllib to get the sprite data from the given url, creates a raw image, and then passes
    it to Tkinter.
    :param url: a string
    :param face: a string
    :precondition: tkinter label sprite_front_img must exist
    :precondition: tkinter label sprite_back_img must exist
    :postcondition: converts image data from link into an image compatible with ImageTk
    :postcondition: configures the sprite_front_img or sprite_back_img label to display image from url
    """
    with urllib.request.urlopen(url) as data:
        image_data = data.read()
    raw_image = Image.open(io.BytesIO(image_data))
    image = ImageTk.PhotoImage(raw_image)
    if face == "front":
        sprite_front_img.configure(image=image)
        sprite_front_img.image = image
    if face == "back":
        sprite_back_img.configure(image=image)
        sprite_back_img.image = image


def get_smogon_info(name: str):
    """Populate smogon info frame with data from Smogon Usage Stats API.

    :param name: a string
    :precondition: name argument must be a string
    :precondition: tkinter label smogon_info must exist
    :postcondition: populates smogon_info label with competitive data for the particular Pokemon
    """
    url = "https://smogon-usage-stats.herokuapp.com/gen8ou/" + name
    res = requests.get(url)
    pokemon = res.json()
    smogon_info["text"] = "GEN 8 COMPETITIVE SMOGON OU SETS\n\n" + smogon_res(pokemon)


def smogon_res(pokemon: dict) -> str:
    """Get Smogon data and return a formatted string.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key pokemon["abilities"] where its value is another dict
    and the keys are strings
    :precondition: pokemon must be a dictionary containing the key pokemon["moves"] where its value is another dict
    and the keys are strings
    :precondition: pokemon must be a dictionary containing the key pokemon["items"] where its value is another dict
    and the keys are strings
    :precondition: all the conditions for the function get_ev to work correctly are met
    :postcondition: converts data into a formatted string
    :postcondition: if data is incomplete, display it as incomplete
    :return: a formatted string with all the Pokemon's competitive information
    """
    try:
        sm_ability = list(pokemon["abilities"].keys())[0]
        sm_moves = ", ".join(list(pokemon["moves"].keys())[0:4])
        sm_item = list(pokemon["items"].keys())[0]
        sm_ev = get_ev(pokemon)
        if len(sm_ability) and len(sm_moves) and len(sm_item) and len(sm_ev) > 0:
            return "Ability: %s \nMoveset: %s \nItem: %s \nSpread: %s" \
                        % (sm_ability, sm_moves, sm_item, sm_ev)
        else:
            return "Incomplete competitive information for this Pokémon."
    except IndexError:
        return "Incomplete competitive information for this Pokémon."


def get_ev(pokemon: dict) -> str:
    """Get recommended nature + EV spread from Smogon Usage Stats API.

    :param pokemon: a dictionary
    :precondition: pokemon must be a dictionary containing the key pokemon["spreads"] where its value is another dict
    and the keys are strings
    :postcondition: converts data into a formatted string
    :postcondition: if data is incomplete, create a string that says so
    :return: a formatted string with all the Pokemon's spread information or stating that the results are incomplete
    """
    try:
        nature = list(pokemon["spreads"].keys())[0]
        ev = list(pokemon["spreads"][nature].keys())[0]
        return nature.capitalize() + ", " + ev
    except IndexError:
        return "Incomplete spread information for this Pokémon."


def no_results():
    """Clear application of all data if no valid response is received.

    :precondition: no preconditions required
    :postcondition: clear the application of all data and images.
    """
    dex_info["text"] = "Info on this Pokémon does not exist."
    smogon_info["text"] = ""
    sprite_front_img.configure(image=None)
    sprite_front_img.image = None
    sprite_back_img.configure(image=None)
    sprite_back_img.image = None
    dex_img.configure(image=None)
    dex_img.image = None


# TKinter Application

root = tk.Tk()

# Prevent window from being resized
root.resizable(False, False)

# Application title and icon
root.title(" Pokédex Application")
root.iconbitmap('poke_icon.ico')

# Application dimensions
canvas = tk.Canvas(root, height=HEIGHT(), width=WIDTH())
canvas.pack()

# Application background
background_image = tk.PhotoImage(file='poke_bg.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relheight=1, relwidth=1)

# Frame for search bar
search_frame = tk.Frame(root, bg=FRAME_COLOR())
search_frame.place(relx=0.05, rely=0.025, relwidth=0.9, relheight=0.08)

# Search bar
search = tk.Entry(search_frame, font=20)
search.place(relx=0.017, rely=0.1, relwidth=0.75, relheight=0.8)

# Search button
search_button = tk.Button(search_frame, text="Search", bg=BUTTON_COLOR(), fg="white",
                          command=lambda: populate_dex(search.get().lower()))
search_button.place(relx=0.78, rely=0.1, relwidth=0.2, relheight=0.8)

# Frame for the pokedex info and official art
info_frame_1 = tk.Frame(root, bg=FRAME_COLOR())
info_frame_1.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.505)

# Pokedex info display
dex_info = tk.Label(info_frame_1, text="To begin, search for a Pokémon by name or dex number!", font=FONT())
dex_info.place(relx=0.38, rely=0.025, relwidth=0.6, relheight=0.95)

# Pokedex image display
dex_img = tk.Label(info_frame_1)
dex_img.place(relx=0.017, rely=0.025, relwidth=0.346, relheight=0.95)

# Frame for Smogon data and game sprites
info_frame_2 = tk.Frame(root, bg=FRAME_COLOR())
info_frame_2.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.32)

# Game sprite display (front and back) - note, there are some issues with S/S exclusive sprites such as bg color
sprite_front_img = tk.Label(info_frame_2, bg="black")
sprite_front_img.place(relx=0.017, rely=0.025, relwidth=0.17, relheight=0.95)
sprite_back_img = tk.Label(info_frame_2, bg="black", fg="white")
sprite_back_img.place(relx=0.195, rely=0.025, relwidth=0.17, relheight=0.95)

# Smogon Gen 8 OU display
smogon_info = tk.Label(info_frame_2, font=FONT())
smogon_info.place(relx=0.38, rely=0.025, relwidth=0.6, relheight=0.95)

root.mainloop()
