# osu-sbgen
a set of classes to help with osu!storyboard generation

## Short rundown on usage
All classes can be instantiated manually, but currently the following structure is being aimed at:
- Storyboard
  - Main container, manages any other containers and knows the `.osu` file and folder structure that you save the sb to in the end
- SBObject
  - Sprites and Animation containers, only collect Commands and decide which to render upon breaking that logic down
- Command
  - Command containers, can be modified / instantiated with their in osu! known syntax - can be managed as objects after that and all heavily rely on the root node's constructor
  - apart from L and T, these are stupid commands -_-
- Command.Builder
  - Factory class to mass produce commands with the same or similar settings
  - this class is aware of the song's timing for now and helps building templates for commands that you use often
 
Main idea of the whole thing is, that all that is needed to be done is instantiating a new storyboard from a Song folder and feeding it a `.osu` file from that folder

After that you can use that container to manage all other containers

Compound effects are planned to be manageable by this root container in the future by extending an interface or inheriting a template effect that takes in parameters and generates multiple commands / sprites

whole framework has not been tested on any full usecase yet so it may be prone to bugs
