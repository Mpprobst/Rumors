# Rumors
Interactive narrative experience that comments on the spread of small town gossip via intelligent agents that create an emergent narrative. Created as a project for Dr. Ware's CS660 course at the University of Kentucky

## Version 0.1
- Player can: Ask characters for rumors, Ask characters for information on thier relationships, and tell their own rumors to others.
- Characters will spread rumors amognst themselves, even making up new ones as they go.

## How to run
- `python source/rumors.py`

### Gameplay Recommendations
- Start by entering `help` for a list of commands.
- Use `look` to see who you can interact with.
- commands are case-sensitive, so always spell proper nouns with the first letter being a capital.
- Address another character by starting the command with their name followed by a comma. Ex: `Blair,`
- End a command with another character followed by a quesiton mark to specify a question about a specific character.
- If telling a rumor, don't end the sentence with any punctuation.
- All text in between should be all lowercase and spelled to the best of your ability.

- You can look into the data structures of all objects with the `info` command. This is meant for debugging and not for gameplay. This will display information that you could otherwise by asking clever questions.

### Examples
- Example command for telling a new rumor: `Blair, Martha robbed Oswald`
- Example command for asking about a relationship: `Blair, how do you feel about Martha?`
- Example command for asking for a rumor about someone: `Blair, what do you know about Martha?`


