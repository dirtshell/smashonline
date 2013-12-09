# smashonline
An easy way for people to arrange Super Smash Bros Melee games online with the [Dolphin Emulator](https://dolphin-emu.org/download/list/old-dc-netplay/1/), implemented using [web.py](http://webpy.org/).

If you cloned this, you are going to need a sqlite database. Simply run <code>cat schema.sql | sqlite3 smashbook.db</code> from the root directory to create your database.

### Things to come
* Allow password protected matches
* Implement CAPTCHAs of some sort
* Creating a match is done in a modal, rather than a seperate page
* Prettify everything
* Autofill the first page of matches with matches in the users region
* Have a page that shows the ELO board
* Implement AJAX so people can view games in other regions

### Maybes
* Implement a user system
* Tie into the Dolphin API to get more information about the matches
  * Winner
  * Players
  * Characters
  * Map
  * Lobby data
