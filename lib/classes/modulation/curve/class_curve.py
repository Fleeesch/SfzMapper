# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Curve
#
#   Contains all the data for a custom curve
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


import math


class Curve():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, instrument, name, curve_type, resolution=1, stepped=False):
        
        # super constructor
        super().__init__()

        # store name, allow index to be set later
        self.instrument = instrument
        self.name = name
        self.index = None

        self.type = curve_type

        # stepped shape
        self.stepped = stepped
        
        # resolution of curve
        self.set_resolution(resolution)

        # increment index if type is indexed
        if self.type == "indexed":
            # apply current index and increment
            self.index = instrument.curve_index
            instrument.curve_index += 1

        # point lookup array
        self.points = []

        # value lookup array (None by default > ignored values)
        self.values = [None] * 128

        # indicates that positions will be automatically calculated
        self.fixed_position = True

        # single point curves
        self.single_point = False

        # curve has net yet been created
        self.created = False

        # add to curve lookup index
        self.instrument.curves[name] = self

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Resolution
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_resolution(self, resolution):
        
        self.resolution = min(max(resolution, 0.01), 1)
        
        self.value_count = round(128 * self.resolution)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Point
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def add_point(self, level, pos=0, exp=1):

        # limit maximum amount of points to 128
        if len(self.points) >= 128:
            return

        # create point and append to lookup list
        self.points.append(self.Point(level, exp, pos))

        # check if there's currently a single point scenario
        if len(self.points) == 1:
            self.single_point = True
        else:
            self.single_point = False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Sort Points
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def sort_points(self):

        # temporary array for storing numbers
        arr_nr = []

        # transfer point positions
        for idx, r in enumerate(self.points):
            arr_nr.append(r.position)

        # sort points based on position, store in new array
        nr_sorted, points_sorted = (list(x) for x in zip(*sorted(zip(arr_nr, self.points), key=lambda pair: pair[0])))

        # overwrite original point lookup array with sorted one
        self.points = points_sorted

        # rewrite point index numbers based on sorted array
        for idx, point in enumerate(self.points):
            point.index = idx

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Interpolate
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def interpolate_points(self):

        # go through points with indexing
        for idx, point in enumerate(self.points):

            # exclude linear progression unless stepped is active
            if point.exponent == 1:
                continue

            # ignore topmost point
            if point.position >= 1:
                continue

            # get next point
            next_point = self.points[idx + 1]
            
            # caculate index delta between points
            delta = next_point.index - point.index - 1
            
            # placeholder for last value
            last_value = None
            
            # go through value range to interpolate
            for i in range(delta):
                
                # calculate factor with reshaped curve characteristics
                factor = pow(i / delta, point.exponent)
                
                # store start and endpoint levels
                level_a = point.level
                level_b = next_point.level
                
                # calculate step value by crossfading between start and end points using the factor
                level = level_a * (1 - factor) + level_b * factor
                
                # only store new value if it differs from the previous value point
                if last_value != level:
                    self.values[point.index + i] = level
                    last_value = level

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Downsample Points
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def downsample_points(self):

        # don't do anything if resolution is set to full
        if self.resolution == 1:
            return

        # get factor for index rescaling
        refactor = 1.0 / self.resolution

        # last point is defaulted to -1 (always process first step)
        last_point = -1

        # init new values index
        values_new = [None] * 128
        
        # always keep the defined start and end
        values_new[0] = self.values[0]
        values_new[127] = self.values[127]
        
        # go through values with by resolution factor reduced count
        for i in range(0, self.value_count):
            
            # calculate point index for original value lookup
            current_point = int(refactor * i)
            
            # check if point differs from last one
            if current_point != last_point:
                # copy point value
                values_new[current_point] = self.values[current_point]
            
            # store last point for comparison
            last_point = current_point
        
        # replace old value array with new one that has the reduced resolution
        self.values = values_new
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Make Stepped
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def make_stepped(self):

        # skip if not stepped
        if not self.stepped:
            return

        # store first value as last value
        last_value = self.values[0]
        
        
        # go through values
        for idx, val in enumerate(self.values):
            
            # skip empty values
            if val is None:
                continue
            
            # value delcared and changed?
            if last_value != val:
                
                # store duplicate of last value
                self.values[idx - 1] = last_value
                
                # update last value
                last_value = val
                
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create (Level Value)
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create(self):

        # skip if there are no points, nothing to create
        if not self.points:
            return

        # sort points based on position
        self.sort_points()

        # go through points
        for idx, point in enumerate(self.points):

            # if an individual position is given unmark fixed position flag
            if idx > 0 and point.position != self.points[idx - 1].position:
                self.fixed_position = False

        # all points share the same position? auto-arrange them
        if self.fixed_position:
            for idx, point in enumerate(self.points):
                point.position = (1 / (len(self.points) - 1)) * idx

        # give clear value borders by default
        self.values[0] = 0
        self.values[127] = 1

        # go through points
        for point in self.points:

            # calculate integer index based on double position
            index = round(point.position * 127)
            
            # get value from point, shave of a few numbers
            self.values[index] = round(point.level, 6)
            
            # overwrite point index with recalculated value index
            point.index = index
        
        # overwrite first and last value with first and last point values
        self.values[0] = self.points[0].level
        self.values[len(self.values) - 1] = self.points[len(self.points) - 1].level

        # interpolate segments, applied only to point with exponent data
        self.interpolate_points()
        
        # reduce resolution if requested
        self.downsample_points()
        
        # make stepped shape if requested
        self.make_stepped()
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get(self):

        # empty string as a base
        data = ""
        
        # add curve index if there is one available
        if self.type == "indexed":
            data += "<curve>\ncurve_index=" + str(self.index) + "\n"

        # go through values
        for idx, value in enumerate(self.values):

            # skip empty values
            if value is None:
                continue

            # number string (changes )
            if self.type != "indexed":
                str_nr = "amp_velcurve_" + str(idx)
            else:
                str_nr = "v" + str(str("%03d" % idx))
            
            # store rounded value string
            str_val = ('%.15f' % value).rstrip('0').rstrip('.')
            
            # store value line using concatenated strings
            data += str_nr + "=" + str_val
            
            if idx <= len(self.values) - 1:
                data += "\n"

        # return sfz-compatible curve segment
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Subclass : Point
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    class Point:

        def __init__(self, level, exp, pos):

            # store basic data
            self.level = level
            self.exponent = exp
            self.position = pos
