# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : LFO
#
#   Custom LFO covered by the SFZ2 Standard
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.lfo.values.elements.class_lfo_offset import LfoOffset
from lib import lookup
from lib.classes.modulation.lfo.sub.class_lfo_sub import LfoSub
from lib.classes.modulation.lfo.values.elements.class_lfo_delay import LfoDelay
from lib.classes.modulation.lfo.values.elements.class_lfo_depth_add import LfoDepthAdd
from lib.classes.modulation.lfo.values.elements.class_lfo_depth import LfoDepth
from lib.classes.modulation.lfo.values.elements.class_lfo_fade import LfoFade
from lib.classes.modulation.lfo.values.elements.class_lfo_phase import LfoPhase
from lib.classes.modulation.lfo.values.elements.class_lfo_rate import LfoRate
from lib.classes.modulation.lfo.values.elements.class_lfo_scale import LfoScale
from lib.classes.modulation.lfo.values.elements.class_lfo_smooth import \
    LfoSmooth
from lib.classes.modulation.lfo.values.elements.class_lfo_step import LfoStep
from lib.classes.modulation.lfo.values.elements.class_lfo_waveform import \
    LfoWaveform
from lib.config.reformat import reformat_modulation_lfo as ref_lfo

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Lfo():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, name, sub_lfo_data, mod_data):

        # self
        self.instrument = instrument
        self.name = name
        
        # modulation data
        self.mod_data = mod_data

        # reformat modulation data
        for mod in self.mod_data:
            self.mod_data[mod] = ref_lfo.reformat_modulation_lfo(self.mod_data[mod])

        # global sub lfo mix-in
        self.sub_lfo_scale = 0

        # store sub-lfo data
        self.sub_lfo_data = sub_lfo_data

        # grab index from instrument
        self.index = instrument.lfo_index

        # increment lfo index of instrument
        instrument.lfo_index += 1

        # store in instrument lfo lookup
        instrument.lfo[name] = self

        # create sfz tag
        self.tag = "lfo" + str(self.index)

        # targets of the lfo
        self.targets = []

        # modulatable attributes
        self.depth_add = LfoDepthAdd(instrument, self)
        self.depth = LfoDepth(instrument, self)
        self.waveform = LfoWaveform(instrument, self)
        self.rate = LfoRate(instrument, self)
        self.delay = LfoDelay(instrument, self)
        self.fade = LfoFade(instrument, self)
        self.phase = LfoPhase(instrument, self)
        self.smooth = LfoSmooth(instrument, self)
        self.offset = LfoOffset(instrument, self)

        # sub lfo lookup
        self.sub_lfo = []

        # load subs if available
        if type(self.sub_lfo_data) is dict:
            self.load_subs()

        # load LFO characteristics modulation
        self.load_modulation()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Subs
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_subs(self):

        # load sub-lfo mix factor
        self.sub_lfo_scale = self.sub_lfo_data["mix"]

        # skip if subs don't have a list
        if type(self.sub_lfo_data["list"]) is not list:
            return

        for idx, sub in enumerate(self.sub_lfo_data["list"]):

            # keep sub lfo count within limit
            if idx + 1 > lookup.ARIA_LFO_SUB_LIMIT:
                break

            try:
                
                # extend with default values if required
                if len(sub) < 1:
                    sub.append(0)
                if len(sub) < 2:
                    sub.append(1)
                if len(sub) < 3:
                    sub.append(0)
                if len(sub) < 3:
                    sub.append(1)

                # create a sub instance
                sub_new = LfoSub(self)

                # ::: Waveform :::

                # use original waveform if excplictly left out
                if sub[0] is None:
                    sub_new.wave = self.waveform.depth

                # try to lookup waveform number if value is string
                elif type(sub[0]) is str:

                    try:
                        sub_new.wave = lookup.LFO_WAVEFORM[sub[0]]
                    except:
                        sub_new.wave = 0

                # use number directly if one is given
                else:
                    sub_new.wave = sub[0]

                # ::: Ratio :::

                # use default value if left out
                if sub[1]:
                    sub_new.ratio = sub[1]
                else:
                    sub_new.ratio = 1

                # ::: Scale :::

                # use default value if left out
                if sub[2]:
                    sub_new.scale = sub[2]
                else:
                    sub_new.scale = ""

                # ::: Offset :::

                # use default value if left out
                if sub[3]:
                    sub_new.offset = sub[3]
                else:
                    sub_new.offset = 0

            except:
                pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Steps
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_steps(self):
        pass
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        data = ""

        data += "// ::: LFO " + str(self.index + 1) + " :::" + "\n"

        # waveform
        data += self.tag + "_wave=" + str(self.waveform.depth) + "\n"
        
        # depth
        data += self.tag + "_freq=" + str(self.rate.depth) + "\n"

        # delay
        data += self.tag + "_delay=" + str(self.delay.depth) + "\n"

        # phase
        data += self.tag + "_phase=" + str(self.phase.depth) + "\n"

        # fade
        data += self.tag + "_fade=" + str(self.fade.depth) + "\n"

        # smooth
        data += self.tag + "_smooth=" + str(self.smooth.depth) + "\n"
        
        # offset
        data += self.tag + "_offset=" + str(self.offset.depth) + "\n"
        
        # subs
        if self.sub_lfo:

            # sub lfo scale
            data += self.tag + "_scale=" + str(self.sub_lfo_scale) + "\n"

            data += "// Sub-LFOs" + "\n"
            
            for sub in self.sub_lfo:
                data += sub.get_sfz()

        # modulation
        mod = self.get_modulation()

        # add modulation lines
        for line in mod:
            data += line + "\n"

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_modulation(self):

        # lookup array for modulation (modulator, lookup name in mod dict)
        mod_list = [
            [self.depth_add, "depth add"],
            [self.depth, "depth"],
            [self.waveform, "waveform"],
            [self.rate, "rate"],
            [self.delay, "delay"],
            [self.fade, "fade"],
            [self.phase, "phase"],
            [self.smooth, "smooth"],
            [self.offset, "offset"]
        ]

        # go through modulation list
        for mod in mod_list:
            # load modulation for element
            mod[0].add_modulation(self.mod_data[mod[1]])
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_modulation(self):
        
        # return line array
        lines = []

        # modulation line array collector
        mod_lines = []

        # lookup array for modulation (modulator, lookup name in mod dict)
        mod_list = [
            self.depth_add,
            self.depth,
            self.waveform,
            self.rate,
            self.delay,
            self.fade,
            self.phase,
            self.smooth,
            self.offset
        ]

        # go through modulation list
        for mod in mod_list:

            # get sfz of modulation
            mod_lines = mod.get_modulation()

            # append lines to return array
            for line in mod_lines:
                lines.append(line)

        return lines
