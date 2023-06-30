# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulatable : Compensation : Sum
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.interfaces.compensation.class_modulatable_compensation import \
    ModulatableCompensation

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ModulatableCompensationSum(ModulatableCompensation):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, source):

        # store refrence
        super().__init__(source)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Compensation Value
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_value(self):

        def collect_data(modulations):

            nonlocal comp_sum

            # go through modulations
            for mod in modulations:

                # check of modulator has modulations itself
                try:
                    # try including the nested modulations
                    if mod.modulations:
                        collect_data(mod.modulations)
                except:
                    pass

                # check if modulation has valid compensation
                if mod.compensation and mod.compensation != 0:

                    # calculate compensation based on compensation factor
                    comp = mod.depth * mod.compensation * -1

                    # add depth to sum, increment count
                    comp_sum += comp

        # sum and count
        comp_sum = 0

        # collect the data
        collect_data(self.source.modulations)

        # return compensation average
        return comp_sum
