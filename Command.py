class Command:

    def __init__(self, t, easing, start_time, end_time):
        # Type and easing
        self.t = t
        self.easing = easing

        # Start and end times of the command
        self.start_time = Command.milliseconds(start_time)
        self.end_time = Command.milliseconds(end_time)

        # Assume start and end were swapped on accident if this is the case
        if self.start_time > self.end_time:
            self.end_time, self.start_time = self.start_time, self.end_time

    def __eq__(self, other):
        return self.start_time == other.start_time and self.end_time == other.end_time and self.t == other.t

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __le__(self, other):
        return self.start_time <= other.start_time

    def __ge__(self, other):
        return self.start_time >= other.start_time

    def __gt__(self, other):
        return self.start_time > other.start_time

    def __ne__(self, other):
        return self.start_time != other.start_time

    def __hash__(self):
        return hash((self.t, self.easing, self.start_time, self.end_time))

    @classmethod
    def milliseconds(cls, time_string) -> int:
        # ascertain that whatever is thrown in is handled as a string and stripped off characters that make no sense
        components = str(time_string).strip('[- ]').split(':')

        # ideally this finds 3, but if the format is given as '332211' or whatever it's already in ms
        if len(components) == 3:  # "mm:ss:ms"
            return int(components[0]) * 60000 + int(components[1]) * 1000 + int(components[2])
        elif len(components) == 1:  # already in ms
            return int(round(float(components[0])))
        return 0  # throw out a 0 in all other cases

    @classmethod
    def get_subclasses_as_dict(cls):
        subclasses = set(cls.__subclasses__())
        ret = dict()
        for subclass in subclasses:
            ret[subclass.__name__] = subclass
        return ret

    # global render command: gives back whatever additional attribs the command has
    def render(self, *args) -> str:
        base_string = ' {},{},{},{}'.format(self.t, self.easing, self.start_time, self.end_time)
        for arg in args:
            base_string += ',{}'.format(arg)
        return base_string


# Fade
class F(Command):

    def __init__(self, easing, start_time, end_time, start_opacity, end_opacity):
        super().__init__('F', easing, start_time, end_time)
        self.s_opacity = F.opacity(float(start_opacity))
        self.e_opacity = F.opacity(float(end_opacity))

    @classmethod
    def opacity(cls, opacity) -> float:
        o = float(opacity)
        if o > 1.0:
            return 1.0
        elif o < 0.0:
            return 0.0
        else:
            return o

    def render(self):
        return super().render(self.s_opacity, self.e_opacity)


# Move (both axis)
class M(Command):

    def __init__(self, easing, start_time, end_time, start_x, start_y, end_x, end_y):
        super().__init__('M', easing, start_time, end_time)
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        self.end_x = int(end_x)
        self.end_y = int(end_y)

    def render(self):
        return super().render(self.start_x, self.start_y, self.end_x, self.end_y)


# MX and MY could be the same class, but aren't for the case where they need different handling of any kind
class MX(Command):
    def __init__(self, easing, start_time, end_time, start_x, end_x):
        super().__init__('MX', easing, start_time, end_time)
        self.start_x = int(start_x)
        self.end_x = int(end_x)

    def render(self):
        return super().render(self.start_x, self.end_x)


class MY(Command):
    def __init__(self, easing, start_time, end_time, start_y, end_y):
        super().__init__('MY', easing, start_time, end_time)
        self.start_y = int(start_y)
        self.end_y = int(end_y)

    def render(self):
        return super().render(self.start_y, self.end_y)


# Scale
class S(Command):
    def __init__(self, easing, start_time, end_time, start_scale, end_scale):
        super().__init__('S', easing, start_time, end_time)
        self.start_scale = S.scale(start_scale)
        self.end_scale = S.scale(end_scale)

    @classmethod
    def scale(cls, scale) -> float:
        s = float(scale)
        if s < 0.0:
            return 0.0
        else:
            return s

    def render(self):
        return super().render(self.start_scale, self.end_scale)


# Vector Scale
class V(Command):
    def __init__(self, easing, start_time, end_time, start_scale_x, start_scale_y, end_scale_x, end_scale_y):
        super().__init__('V', easing, start_time, end_time)
        self.start_scale_x = S.scale(start_scale_x)
        self.end_scale_x = S.scale(end_scale_x)
        self.start_scale_x = S.scale(start_scale_y)
        self.end_scale_x = S.scale(end_scale_y)

    def render(self):
        return super().render(self.start_scale_x, self.start_scale_y, self.end_scale.x, self.end_scale_y)


class R(Command):
    def __init__(self, easing, start_time, end_time, start_rotate, end_rotate):
        super().__init__('R', easing, start_time, end_time)
        self.start_rotate = float(start_rotate)
        self.end_rotate = float(end_rotate)

    def render(self):
        return super().render(self.start_rotate, self.end_rotate)


class C(Command):
    def __init__(self, easing, start_time, end_time, s_rgb, e_rgb):
        super().__init__('C', easing, start_time, end_time)
        self.start_rgb = (C.rgb(s_rgb[0]), C.rgb(s_rgb[1]), C.rgb(s_rgb[2]))
        self.end_rgb = (C.rgb(e_rgb[0]), C.rgb(e_rgb[1]), C.rgb(e_rgb[2]))

    # alternate Constructor
    @classmethod
    def from_hex(cls, easing, start_time, end_time, start_hex, end_hex):
        start_rgb = C.hex_to_rgb(start_hex)
        end_rgb = C.hex_to_rgb(end_hex)

        return cls(easing, start_time, end_time, start_rgb, end_rgb)

    def render(self):
        return super().render(self.start_rgb[0], self.start_rgb[1], self.start_rgb[2],
                              self.end_rgb[0], self.end_rgb[1], self.end_rgb[2])

    @classmethod
    def rgb(cls, value):
        v = int(value)
        if v > 255:
            v = 255
        if v < 0:
            v = 0
        return v

    @classmethod
    def hex_to_rgb(cls, hx):
        stripped = str(hx).lstrip('#')
        tup = tuple(int(stripped[i:i+2], 16) for i in (0, 2, 4) if len(stripped[i:i+2]) == 2)
        while len(tup) < 3:
            tup = tup + (0,)

        return tup


class P(Command):
    def __init__(self, easing, start_time, end_time, param):
        super().__init__('C', easing, start_time, end_time)
        self.param = str(param).upper()

    def render(self):
        return super().render(self.param)


class L(Command):
    def __init__(self, start_time, loop_count):
        self.start_time = Command.milliseconds(start_time)
        self.loop_count = int(loop_count)
        self.commands = []

    def add(self, command):
        if isinstance(command, Command):
            self.commands.append(command)

    def rem(self, command):
        if isinstance(command, Command):
            self.commands.remove(command)

    # this actually needs to filter its children the same way sprites do but I didn't implement that yet
    # maybe I can reuse the sprite's checks and isolate that functionality somewhere else
    def render(self):
        format_str = ' L,{},{}'.format(self.start_time, self.loop_count)
        for command in self.commands:
            format_str += '\n ' + command.render()
        return format_str


class Factory:
    def __init__(self, timing):
        self.timing_points = timing     # dictionary containing all timing points of a song
        self.t = None                   # type of the command to be generated, determines what is used upon rendering
        self.ease = None                # Easing
        self.start_time = None          # start time in ms
        self.dura = None                # duration in beats, if this is set the class will ignore the end and calc it
        self.end_time = None            # endtime
        self.tupS = None                # tuple representing the start parameters of the command
        self.tupE = None                # tuple representing the end parameters of the command

    # sets the type
    def type(self, t):
        self.t = t
        return self

    # sets the start
    def start(self, time):
        self.start_time = Command.milliseconds(time)
        return self

    # sets the end and resets the duration if specified because otherwise the end will be ignored
    def end(self, time):
        self.end_time = Command.milliseconds(time)
        self.dura = None
        return self

    # sets the duration relative to the start time
    def duration(self, duration_string):
        # split the fraction into numerator and enumerator
        dur = duration_string.split('/')

        # nothing makes sense if you don't pass in a fraction
        if len(dur) == 2:
            self.dura = dur
            self.end_time = None

        # return reference to self
        return self

    # calculates the end time if the duration is set and returns that
    def calc_end_time(self):
        if self.dura is not None:
            # init relevant start dict
            relevant_timing_point = {}

            # start is set to something already
            if self.start_time is not None:
                # loop over timing points until the first timing point that
                # applies to the relevant starting section is hit
                for timing_point, content in self.timing_points.items():
                    if content['offset'] <= self.start_time:
                        relevant_timing_point = content
                        break   # kill loop upon first match

            # pretend reference is initial and just refer to the
            # bpm settings of the last timing point if nothing was found
            if relevant_timing_point == {}:
                relevant_timing_point = self.timing_points[0]

            # e.g. 400 ms per beat * 1 / 2 = half a beat if 1 beat is 400 ms
            return self.start_time + (relevant_timing_point['ms'] * float(self.dura[0]) / float(self.dura[1]))
        if self.end_time is not None:
            return self.end_time
        return 0

    # only relevant for C (start and end color)
    def color_start(self, r, g, b):
        self.tupS = (r, g, b)
        return self

    def color_end(self, r, g, b):
        self.tupE = (r, g, b)
        return self

    def color_start(self, hex_color):
        self.tupS = C.hex_to_rgb(hex_color)
        return self

    def color_end(self, hex_color):
        self.tupE = C.hex_to_rgb(hex_color)
        return self

    # only relevant for Move (start/end positions)
    def start_x(self, start_x):
        self.tupS = (int(start_x),)
        return self

    def end_x(self, end_x):
        self.tupE = (int(end_x),)
        return self

    def start_y(self, start_y):
        return self.start_x(start_y)

    def end_y(self, end_y):
        return self.end_x(end_y)

    def start_coord(self, start_coord):
        self.tupS = (int(start_coord[0]), int(start_coord[1]))
        return self

    def end_coord(self, end_coord):
        self.tupE = (int(end_coord[0]), int(end_coord[1]))
        return self

    # Scaling
    def start_s(self, start_s):
        self.tupS = (S.scale(start_s),)
        return self

    def end_s(self, end_s):
        self.tupE = (S.scale(end_s),)
        return self

    # Vector scaling
    def star_v(self, start_vector):
        self.tupS = (S.scale(start_vector[0]), S.scale(start_vector[1]))
        return self

    def end_v(self, end_vector):
        self.tupE = (S.scale(end_vector[0]), S.scale(end_vector[1]))
        return self

    # Rotate
    def start_r(self, start_r):
        self.tupS = (float(start_r),)
        return self

    def end_r(self, end_r):
        self.tupE = (float(end_r),)
        return self

    # Fade
    def start_o(self, start_o):
        self.tupS = (F.opacity(start_o),)
        return self

    def end_o(self, end_o):
        self.tupE = (F.opacity(end_o),)
        return self

    def easing(self, easing):
        self.ease = int(easing)
        return self

    def reset(self):
        self.__init__(self.timing_points)

    # builds from the parameters it knows
    def build(self):
        # get all current attributes to the local scope to not accidentally modify class attributes which could cause
        # different results upon running
        t = self.t                      # type
        start = self.start_time         # start time
        end = self.calc_end_time()      # calculated end time
        easing = self.ease              # easing
        start_params = self.tupS        # tuple with start values
        end_params = self.tupE          # tuple with end values
        subclasses = Command.get_subclasses_as_dict()

        if end_params is None and start_params is not None: end_params = start_params
        if start is None: start = 0
        if easing is None: easing = 0

        # type has to be set or else the builder doesnt know what the actual arguments mean
        if t == "F" or t == "MX" or t == "S" or t == "R":  # subclasses with 2 params take the first tuple entry
            if len(start_params) <= 2 and len(end_params) <= 2:
                return subclasses[t](easing, start, end, start_params[0], end_params[0])
        elif t == "M" or t == "V":                         # subclasses expecting 2 params need two to be set
            if len(start_params) == 2 and len(end_params) == 2:
                return subclasses[t](easing, start, end, start_params[0], start_params[1],
                                     end_params[0], end_params[1])
        elif t == "MY":                                    # subclass that takes the last available (y coord)
            param_s = 0
            param_e = 0
            if start_params is not None and end_params is not None:
                if len(start_params) == 1: param_s = start_params[0]
                elif len(start_params) == 2: param_s = start_params[1]
                if len(end_params) == 1: param_e = end_params[0]
                elif len(end_params) == 2: param_e = end_params[1]
                return subclasses[t](easing, start, end, param_s, param_e)
        elif t == "C":                                      # subclass expecting 3 values
            if len(start_params) == 3 and len(end_params) == 3:
                return subclasses[t](easing, start, end, start_params[0], start_params[1], start_params[2],
                                     end_params[0], end_params[1], end_params[2])

        # if the code makes it to here it didn't return any command so far, at that point it should fail over and
        # give the caller stack tracing information
        raise ValueError('The command couln\'t be built because it is either '
                         'unknown to the builder or is missing required arguments',
                         self.t, self.easing, self.start_time, self.end_time, self.tupS, self.tupE)



