# Tectonic Turtle Bingo

These notes were originally just a ramble of general thoughts and ideas.

## Questions

- Database / Datastorage? (SQLite / JSON) KEEP IT SIMPLE
- Language? (Probably Python for the image manipulation ease)
- Print out bingo board as an image instead of website?
- Unlockable help commands for each tile
- Unlockable commands based on tile completion (By tile number, one command)
- Submissions with bot (Admin only? Would allow for more trust for automatic flip)
- How do we handle multi-part tiles?
- Tile states... Unlocked, Locked, Completed
- Item submission names are easy, how about minigames, CAs, XP tiles?

## Answers

- Require typing the item/drop name WORD FOR WORD, EXACT MATCH. ex: options["Dizana's quiver"]
- Example submission `/submit "Dizana's quiver" "screenshot.png"`
- Items: Exact name, CAs and Minigames etc: Exact key given by `/tile` command
    - How to handle situations like "This drop can be used in many tiles" (Avoid?)

## Command -> Functionality

### Users

- `/submit {item_name} {screenshot_file}` for submitting tiles
    - Only works in submission channel
    - Trust or Verify? (Keep trusted IDs and if all offline, trust)
    - Unsubmit option
    - Check if tile is complete
    - Store tile submitter
    - Post confirmation message which posts the screenshot (Verify usability on mobile)
    - Store in datastorage (Store link to confirmation message)
    - Multi-part tiles (Such as sweets, Barrows tiles, slayer uniques)
    - On completion, send unlocked tiles to specified channel
    - Clear error messages for when tile failed to submit

- `/tile {id}` for help about tiles
    - Do not show if "requirements" not met (How to check requirements in a graph? `if (adjacent.any().complete) return info()`)
    - Show embed of tile rules, icon, and information
    - EXTRA, if completed show information about related submissions and completer name
    - For non item specific tiles, list the submission key ex: "I am a Combat Achievement", "Penance Queen Kill"
    - Show progression of the tile, seems like a must have for clarity

- `/list {tiles|tasks}`
    - Display all tiles that have the "Unlocked" state
    - Display all tasks of tiles?
    - Dislay tile IDs

### Admins

- `/unsubmit "Dizana's quiver"` Uncomplete tile (Don't wipe progress, only hide again)

## Data structure and algorithm stuff

### Questions

- How do we easily and reasonably store tile data? (Graph i guess)
- How do we easily check if a nearby tile is complete
- How to handle unlocking tiles once adjacent onces are complete

### Answers

- Verbose data objects
