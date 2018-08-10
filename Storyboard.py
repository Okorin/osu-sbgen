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
        with open(self.song_folder + timing_point_file, 'r') as file:
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
        for sprite in self.sprites:
            output += sprite.render()

        return output

    def new_sprite(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], x=320, y=240):
        """
        instantiates a new sprite
        :param path: filepath to the sprite relative from the SB folder path
        :param layer: SB Layer the sprite plays on
        :param origin: where the 'center' point of the sprite is
        :param x: default coordinate x
        :param y: default coordinate y
        :return: sprite instance
        """
        sprite = Object.Sprite(self.sb_folder + path, layer, origin, x, y)
        self.sprites.append(sprite)
        self.current_sprite = sprite
        return sprite

    def new_animation(self, path, layer=Constants.la['bg'], origin=Constants.o['cc'], frame_count=2, frame_delay=500,
                      loop_type="LoopForever", x=320, y=240):
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
        :return: animation instance
        """
        animation = Object.Animation(self.sb_folder + path, layer, origin, frame_count, frame_delay, loop_type, x, y)
        self.sprites.append(animation)
        self.current_sprite
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
        with open(self.song_folder + self.osb_file_name, 'w') as file:
            for sprite in self.sprites:
                file.write(sprite.render())


'''
Example usage:
sb = Storyboard("G:\osu!\Songs\\4_Elements_-_I_Want_You_To_Hold_Me_Nightcore_Mix",
                "4 Elements - I Want You To Hold Me (Nightcore Mix) (Okoratu) [Insane].osu")

factory = sb.new_command_factory()
print(factory.type("M")
      .start_coord((300, 200))
      .end_coord((320, 240))
      .start("00:13:281 - ")
      .duration("2/1")
      .easing(1)
      .build().render())
print(factory.start("00:14:690 - ").build().render())
print(factory.type("MX").build().render())
print(factory.type("MY").build().render())
'''
