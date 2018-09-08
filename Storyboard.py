import Constants
import Object
import Command


class Storyboard:
    def __init__(self, song_folder, timing_point_file, sb_folder=""):

        # reformat song_folder if it's not ending in /
        if song_folder[-1:] != '\\' or song_folder[-1:] != '/':
            song_folder += '/'

        # song and sb file paths, the sb folder is expected to be relative
        self.song_folder = song_folder
        self.sb_folder = sb_folder

        # List to hold all sprites
        self.sprites = list()
        self.current_sprite = None

        # effects
        self.effects = list()

        # all timing points of the difficulty
        self.timing_points = dict()

        # file name of the .osb
        self.osb_file_name = str()

        # just read the .osu provided into the file
        self.parse_osu_difficulty(timing_point_file)

    def parse_osu_difficulty(self, timing_point_file):

        # start reading?
        start = 0

        # timing point index
        i = 0

        # difficulty name
        ver = str()

        # get the timing points from an .osu in the folder
        with open(self.song_folder + timing_point_file, 'r', encoding="utf8") as file:
            for line in file:
                if 'Version:' in line:  # difficulty name
                    ver += line.strip('Version:')
                if '[Colours]\n' == line:  # anything after this is not interesting
                    break
                elif start == 1:  # reading started?
                    parameters = line.split(',')
                    # the last line is just an empty line so it'll hold \n only and thus only create 1 element
                    if len(parameters) == 8 and int(parameters[6]) == 1:
                        self.timing_points[i] = dict()
                        self.timing_points[i]['offset'] = int(parameters[0])  # offset of the timing point
                        self.timing_points[i]['ms'] = float(parameters[1])  # ms per beat
                        self.timing_points[i]['bpm'] = round(60000 / float(parameters[1]), 3)  # bpm rounded to 3 last
                        self.timing_points[i]['meter'] = int(parameters[2])  # the meter of the song
                        self.timing_points[i]['sample'] = int(parameters[3])  # sampleset of the line
                        self.timing_points[i]['sindex'] = int(parameters[4])  # sampleset index
                        self.timing_points[i]['vol'] = int(parameters[5])  # volume
                        self.timing_points[i]['inherit'] = int(parameters[6])  # inherited point?
                        self.timing_points[i]['kiai'] = int(parameters[7])  # kiai mode
                        i += 1
                elif '[TimingPoints]' in line:  # ensure to start reading after the timing points line
                    start = 1

        # deduce the name the .osb file needs to have based on the difficulty filename it has received
        self.osb_file_name = timing_point_file.strip(' [' + ver + '].osu') + '.osb'

    def render(self):
        """
        kickstarts rendering all children

        :return: the whole output the SB knows as a string
        """
        output = str()

        # render all effects
        for effect in self.effects:
            spr = effect.get_sprites()
            for sprite in spr:
                output += sprite.render()

        # all sprites
        for sprite in self.sprites:
            output += sprite.render()

        return output

    def new_sprite(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], x=320, y=240, use_folder=True):
        """
        instantiates a new sprite
        :param path: filepath to the sprite relative from the SB folder path
        :param layer: SB Layer the sprite plays on
        :param origin: where the 'center' point of the sprite is
        :param x: default coordinate x
        :param y: default coordinate y
        :param use_folder: determines whether or not to use the SB folder
        :return: sprite instance
        """
        if use_folder:
            sprite = Object.Sprite(self.sb_folder + path, layer, origin, x, y)
        else:
            sprite = Object.Sprite(path, layer, origin, x, y)
        self.sprites.append(sprite)
        self.current_sprite = sprite
        return sprite

    def new_animation(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], frame_count=2, frame_delay=500,
                      loop_type="LoopForever", x=320, y=240, use_folder=True):
        """
        instantiates a new sprite
        :param path: filepath to the sprite relative from the SB folder path
        :param layer: SB Layer the sprite plays on
        :param origin: where the 'center' point of the sprite is
        :param frame_count: # of animation frames
        :param frame_delay: # delay between frames
        :param loop_type:  loop forever or just once?
        :param x: default coordinate x
        :param y: default coordinate y
        :param use_folder: determine whether or not to use the SB folder known by this class
        :return: animation instance
        """
        if use_folder:
            animation = Object.Animation(self.sb_folder + path, layer, origin, frame_count, frame_delay, loop_type, x, y)
        else:
            animation = Object.Animation(path, layer, origin, frame_count, frame_delay, loop_type, x, y)
        self.sprites.append(animation)
        self.current_sprite = animation
        return animation

    def new_command_factory(self):
        """
        creates a new timeline-aware command factory without anything in it
        :return:
        """
        return Command.Factory(self.timing_points)

    def to_osb(self):
        """
        renders each sprite in chunks to an .osb file
        """
        with open(self.song_folder + self.osb_file_name, 'w', encoding='utf8') as file:
            file.write("[Events]\n")
            # render all sprites
            for sprite in self.sprites:
                file.write(sprite.render())
            # render all effects
            for effect in self.effects:
                spr = effect.get_sprites()
                for sprite in spr:
                    file.write(sprite.render())

    def append_effect(self, effect):
        effect.apply()
        self.effects.append(effect)

