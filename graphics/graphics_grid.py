from graphics.graphics_text import *


class GraphicsGrid:
    """
    This class holds the current grid displayed in the canvas
    """
    def __init__(self):
        # Save the current camera settings
        self.camera_pos = scene.camera.pos
        self.camera_axes = scene.camera.axis
        # Initialise a grid object
        self.grid_object = [[], []]
        self.__init_grid()

    def __init_grid(self):
        """
        Initialise the grid along the x, y, z axes.
        """
        num_squares = 10  # Length of the grid in each direction (in units)
        relative_cam = True  # Whether the grid follows the camera rotation and movement

        the_grid = self.__create_grid_objects(relative_cam, num_squares)
        self.grid_object[0] = the_grid

        # Update the labels instead of recreating them
        update_grid_numbers(self.grid_object[1], relative_cam, num_squares)

    def __create_grid_objects(self, bool_camera_relative, num_squares):
        """
        Draw a grid along each 3D plane, that is closest to the camera.

        :param bool_camera_relative: Whether to draw the axes at the camera focus point or at (0, 0, 0).
        :type bool_camera_relative: bool
        :param num_squares: How many unit squares to draw along the axis.
        :type num_squares: int
        :return: List of the three drawn axes.
        :rtype: list
        """

        # Initial conditions
        xz_lines = []
        xy_lines = []
        yz_lines = []
        camera_axes = self.camera_axes
        # Locate centre of axes
        if bool_camera_relative:
            x_origin, y_origin, z_origin = round(scene.center.x), round(scene.center.y), round(scene.center.z)
        else:
            x_origin, y_origin, z_origin = 0, 0, 0

        #   CAMERA AXES |  DISPLAYED GRID | XZ PLANE | XY PLANE | YZ PLANE
        #      x,y,z    |      x,y,z      |   x,z    |    x,y   |    y,z
        #  -------------+-----------------+----------+----------+----------
        #      -,-,-    |      +,+,+      |   +,+    |    +,+   |    +,+
        #      -,-,+    |      +,+,-      |   +,-    |    +,+   |    +,-
        #      -,+,-    |      +,-,+      |   +,+    |    +,-   |    -,+
        #      -,+,+    |      +,-,-      |   +,-    |    +,-   |    -,-
        #      +,-,-    |      -,+,+      |   -,+    |    -,+   |    +,+
        #      +,-,+    |      -,+,-      |   -,-    |    -,+   |    +,-
        #      +,+,-    |      -,-,+      |   -,+    |    -,-   |    -,+
        #      +,+,+    |      -,-,-      |   -,-    |    -,-   |    -,-
        # min = -num_squares or 0, around the default position
        # max = +num_squares or 0, around the default position
        # e.g. at the origin, for negative axes: -10 -> 0, positive axes: 0 -> 10
        min_x_coord = x_origin + int(-(num_squares / 2) + (sign(camera_axes.x) * -1) * (num_squares / 2))
        max_x_coord = x_origin + int((num_squares / 2) + (sign(camera_axes.x) * -1) * (num_squares / 2))

        min_y_coord = y_origin + int(-(num_squares / 2) + (sign(camera_axes.y) * -1) * (num_squares / 2))
        max_y_coord = y_origin + int((num_squares / 2) + (sign(camera_axes.y) * -1) * (num_squares / 2))

        min_z_coord = z_origin + int(-(num_squares / 2) + (sign(camera_axes.z) * -1) * (num_squares / 2))
        max_z_coord = z_origin + int((num_squares / 2) + (sign(camera_axes.z) * -1) * (num_squares / 2))

        # XZ plane
        for x_point in range(min_x_coord, max_x_coord + 1):
            # Draw a line across for each x coord, along the same y-axis, from min to max z coord
            xz_lines.append(create_line(
                vector(x_point, y_origin, min_z_coord),
                vector(x_point, y_origin, max_z_coord)
            ))
        for z_point in range(min_z_coord, max_z_coord + 1):
            # Draw a line across each z coord, along the same y-axis, from min to max z coord
            xz_lines.append(create_line(
                vector(min_x_coord, y_origin, z_point),
                vector(max_x_coord, y_origin, z_point)
            ))

        # XY plane
        for x_point in range(min_x_coord, max_x_coord + 1):
            # Draw a line across each x coord, along the same z-axis, from min to max y coord
            xy_lines.append(create_line(
                vector(x_point, min_y_coord, z_origin),
                vector(x_point, max_y_coord, z_origin)
            ))
        for y_point in range(min_y_coord, max_y_coord + 1):
            # Draw a line across each y coord, along the same z-axis, from min to max x coord
            xy_lines.append(create_line(
                vector(min_x_coord, y_point, z_origin),
                vector(max_x_coord, y_point, z_origin)
            ))

        # YZ plane
        for y_point in range(min_y_coord, max_y_coord + 1):
            # Draw a line across each y coord, along the same x-axis, from min to max z coord
            yz_lines.append(create_line(
                vector(x_origin, y_point, min_z_coord),
                vector(x_origin, y_point, max_z_coord)
            ))
        for z_point in range(min_z_coord, max_z_coord + 1):
            # Draw a line across each z coord, along the same x-axis, from min to max y coord
            yz_lines.append(create_line(
                vector(x_origin, min_y_coord, z_point),
                vector(x_origin, max_y_coord, z_point)
            ))

        # Compound the lines together into respective objects
        xz_plane = compound(xz_lines)
        xy_plane = compound(xy_lines)
        yz_plane = compound(yz_lines)

        # Combine all into one list
        grid = [xy_plane, xz_plane, yz_plane]

        return grid

    def __move_grid_objects(self, bool_camera_relative, num_squares):
        camera_axes = self.camera_axes
        # Locate centre of axes
        if bool_camera_relative:
            x_origin, y_origin, z_origin = round(scene.center.x), round(scene.center.y), round(scene.center.z)
        else:
            x_origin, y_origin, z_origin = 0, 0, 0

        #   CAMERA AXES |  DISPLAYED GRID | XZ PLANE | XY PLANE | YZ PLANE
        #      x,y,z    |      x,y,z      |   x,z    |    x,y   |    y,z
        #  -------------+-----------------+----------+----------+----------
        #      -,-,-    |      +,+,+      |   +,+    |    +,+   |    +,+
        #      -,-,+    |      +,+,-      |   +,-    |    +,+   |    +,-
        #      -,+,-    |      +,-,+      |   +,+    |    +,-   |    -,+
        #      -,+,+    |      +,-,-      |   +,-    |    +,-   |    -,-
        #      +,-,-    |      -,+,+      |   -,+    |    -,+   |    +,+
        #      +,-,+    |      -,+,-      |   -,-    |    -,+   |    +,-
        #      +,+,-    |      -,-,+      |   -,+    |    -,-   |    -,+
        #      +,+,+    |      -,-,-      |   -,-    |    -,-   |    -,-
        # min = -num_squares or 0, around the default position
        # max = +num_squares or 0, around the default position
        # e.g. at the origin, for negative axes: -10 -> 0, positive axes: 0 -> 10
        min_x_coord = x_origin + int(-(num_squares / 2) + (sign(camera_axes.x) * -1) * (num_squares / 2))
        max_x_coord = x_origin + int((num_squares / 2) + (sign(camera_axes.x) * -1) * (num_squares / 2))

        min_y_coord = y_origin + int(-(num_squares / 2) + (sign(camera_axes.y) * -1) * (num_squares / 2))
        max_y_coord = y_origin + int((num_squares / 2) + (sign(camera_axes.y) * -1) * (num_squares / 2))

        min_z_coord = z_origin + int(-(num_squares / 2) + (sign(camera_axes.z) * -1) * (num_squares / 2))
        max_z_coord = z_origin + int((num_squares / 2) + (sign(camera_axes.z) * -1) * (num_squares / 2))

        x_middle = (max_x_coord + min_x_coord) / 2
        y_middle = (max_y_coord + min_y_coord) / 2
        z_middle = (max_z_coord + min_z_coord) / 2

        # XY Plane
        if camera_axes.z < 0:
            self.grid_object[0][0].pos = vector(x_middle, y_middle, min_z_coord)
        else:
            self.grid_object[0][0].pos = vector(x_middle, y_middle, max_z_coord)

        # XZ Plane
        if camera_axes.y < 0:
            self.grid_object[0][1].pos = vector(x_middle, min_y_coord, z_middle)
        else:
            self.grid_object[0][1].pos = vector(x_middle, max_y_coord, z_middle)

        # YZ Plane
        if camera_axes.x < 0:
            self.grid_object[0][2].pos = vector(min_x_coord, y_middle, z_middle)
        else:
            self.grid_object[0][2].pos = vector(max_x_coord, y_middle, z_middle)

    def update_grid(self):
        """
        Update the grid axes and numbers if the camera position/rotation has changed.

        """

        # Obtain the new camera settings
        new_camera_pos = scene.camera.pos
        new_camera_axes = scene.camera.axis

        old_camera_pos = self.camera_pos
        old_camera_axes = self.camera_axes

        # If camera is different to previous: update
        if (not new_camera_axes.equals(old_camera_axes)) or (not new_camera_pos.equals(old_camera_pos)):
            # Update old positions
            self.camera_pos = new_camera_pos
            self.camera_axes = new_camera_axes

            # Update grid
            num_squares = 10  # Length of the grid in each direction (in units)
            relative_cam = True  # Whether the grid follows the camera rotation and movement
            self.__move_grid_objects(relative_cam, num_squares)
            update_grid_numbers(self.grid_object[1], relative_cam, num_squares)

        # Else save current grid
        else:
            # Already current
            pass

    def set_visibility(self, is_visible):
        """
        Set the visibility of the grid

        :param is_visible: Boolean of whether to display the grid
        :type is_visible: bool
        """
        for plane in self.grid_object[0]:
            plane.visible = is_visible
        for number in self.grid_object[1]:
            number.visible = is_visible
        
    def clear_scene(self):
        """
        Clear the canvas of all objects (keeping the grid)

        Due to how VPython operates, there is no 'deletion' of objects directly.
        To 'delete' objects, first they must be rendered invisible.

        Then: if a new object with the same variable name is used, the previous memory will be freed.
        Or: del variable_name will free its memory.
        If the object wasn't invisible, it would remain visible in the scene.

        Since the scene doesnt track variable names, the best way to clear the scene is to render all objects invisible,
        and have the user assume they are all deleted. However, all objects can be redisplayed by setting the visibility
        """
        # Save current grid visibility
        grid_visibility = self.grid_object[0][0].visible

        # Set all objects invisible
        for scene_object in scene.objects:
            scene_object.visible = False

        # Set grid visibility to previous
        self.set_visibility(grid_visibility)


def create_line(pos1, pos2):
    """
    Create a line from position 1 to position 2.

    :param pos1: 3D position of one end of the line.
    :type pos1: class:`vpython.vector`
    :param pos2: 3D position of the other end of the line.
    :type pos2: class:`vpython.vector`
    """

    # Length of the line using the magnitude
    line_len = mag(pos2-pos1)

    # Position of the line is the midpoint (centre) between the ends
    position = (pos1 + pos2) / 2

    # Axis direction of the line (to align the box (line) to intersect the two points)
    axis_dir = pos2 - pos1

    # Return a box of thin width and height to resemble a line
    thickness = 0.01
    return box(pos=position, axis=axis_dir, length=line_len, width=thickness, height=thickness, color=color.black)
