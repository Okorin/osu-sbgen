import Constants


class SBObj:
    def __init__(self, t, path, layer=Constants.la['bg'], origin=Constants.o['cc'], x=320, y=240):
        self.t = t
        self.layer = layer
        self.origin = origin
        self.path = path
        self.x = x
        self.y = y
        self.commands = list()

    def append(self, command):
        self.commands.append(command)

    def pluck(self, command):
        self.commands.pluck(command)

    def render(self, *args):
        """
        renders the sprite and all children
        :param args: additional arguments to be rendered
        :return: the whole SBObject rendered
        """
        # start with base arguments
        rendered_string = '{},{},{},"{}",{},{}'.format(self.t, self.layer, self.origin, self.path, self.x, self.y)

        # add all other arguments at the end
        for arg in args:
            rendered_string += ',{}'.format(arg)

        # new line
        rendered_string += '\n'

        # sorting commands compares start time!
        # equality check for commands compares TYPE, so this removes duplicate commands and sorts by time
        self.commands = sorted(set(self.commands))

        # selectively decide on which command to render
        for command in self.commands:

            # filter through all commands attached to the Object. Compare their typing and if
            # another command of the same type is starting before or after it
            matches = [comm for comm in self.commands if comm.t == command.t and
                       comm.start_time < command.start_time and comm.end_time > command.end_time
                       and comm is not command]

            # i didnt want to switch the logic of this around so
            # this must return no matches in order to decide a command is worth rendering
            if len(matches) == 0:
                rendered_string += command.render() + '\n'

        return rendered_string + '\n'


# Sprites are the bare minimum object and dont really do much else from their base
class Sprite(SBObj):
    def __init__(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], x=320, y=240):
        super().__init__('Sprite', path, layer, origin, x, y)

    def render(self):
        return super().render()


# Animations don't do much more too apart from having more attributes
class Animation(SBObj):
    def __init__(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], frame_count=2, frame_delay=500,
                 loop_type="LoopForever", x=320, y=240):
        super().__init__('Animation', path, layer, origin, x, y)
        self.frame_count = int(frame_count)
        self.frame_delay = int(frame_delay)
        self.loop_type = str(loop_type)

    def render(self):
        return super().render(self.frame_count, self.frame_delay, self.loop_type)

