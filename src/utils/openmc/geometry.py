from xml.etree import ElementTree as ET

import openmc
from openmc.clean_xml import *


def reset_auto_ids():
    openmc.reset_auto_material_id()
    openmc.reset_auto_surface_id()
    openmc.reset_auto_cell_id()
    openmc.reset_auto_universe_id()


class Geometry(object):

    def __init__(self):

        # Initialize Geometry class attributes
        self._root_universe = None
        self._offsets = {}


    @property
    def root_universe(self):
        return self._root_universe


    @root_universe.setter
    def root_universe(self, root_universe):

        if not isinstance(root_universe, openmc.Universe):
            msg = 'Unable to add root Universe {0} to Geometry since ' \
                  'it is not a Universe'.format(root_universe)
            raise ValueError(msg)

        elif root_universe._id != 0:
            msg = 'Unable to add root Universe {0} to Geometry since ' \
                  'it has ID={1} instead of ' \
                  'ID=0'.format(root_universe, root_universe._id)
            raise ValueError(msg)

        self._root_universe = root_universe


    def get_offset(self, path, filter_offset):
        """
        Returns the corresponding location in the results array for a given
        path and filter number.

        Parameters
        ----------
        path : list
                A list of IDs that form the path to the target. It should begin
                with 0 for the base universe, and should cover every universe,
                cell, and lattice passed through. For the case of the lattice,
                a tuple should be provided to indicate which coordinates in the
                lattice should be entered. This should be in the
                form: (lat_id, i_x, i_y, i_z)

        filter_offset : int
                An integer that specifies which offset map the filter is using

        """

        # Return memoize'd offset if possible
        if (path, filter_offset) in self._offsets:
            offset = self._offsets[(path, filter_offset)]

        # Begin recursive call to compute offset starting with the base Universe
        else:
            offset = self._root_universe.get_offset(path, filter_offset)
            self._offsets[(path, filter_offset)] = offset

        # Return the final offset
        return offset


    def get_all_cells(self):
        return self._root_universe.get_all_cells()


    def get_all_universes(self):
        return self._root_universe.get_all_universes()


    def get_all_nuclides(self):

        nuclides = {}
        materials = self.get_all_materials()

        for material in materials:
            nuclides.update(material.get_all_nuclides())

        return nuclides


    def get_all_materials(self):

        material_cells = self.get_all_material_cells()
        materials = set()

        for cell in material_cells:
            materials.add(cell._fill)

        return list(materials)


    def get_all_material_cells(self):

        all_cells = self.get_all_cells()
        material_cells = set()

        for cell_id, cell in all_cells.items():
            if cell._type == 'normal':
                material_cells.add(cell)

        return list(material_cells)


    def get_all_material_universes(self):

        all_universes = self.get_all_universes()
        material_universes = set()

        for universe_id, universe in all_universes.items():

            cells = universe._cells

            for cell_id, cell in cells.items():
                if cell._type == 'normal':
                    material_universes.add(universe)

        return list(material_universes)



class GeometryFile(object):

    def __init__(self):

        # Initialize GeometryFile class attributes
        self._geometry = None
        self._geometry_file = ET.Element("geometry")


    @property
    def geometry(self):
        return self._geometry


    @geometry.setter
    def geometry(self, geometry):

        if not isinstance(geometry, Geometry):
            msg = 'Unable to set the Geometry to {0} for the GeometryFile ' \
                        'since it is not a Geometry object'.format(geometry)
            raise ValueError(msg)

        self._geometry = geometry


    def export_to_xml(self):

        root_universe = self._geometry._root_universe
        root_universe.create_xml_subelement(self._geometry_file)

        # Clean the indentation in the file to be user-readable
        sort_xml_elements(self._geometry_file)
        clean_xml_indentation(self._geometry_file)

        # Write the XML Tree to the materials.xml file
        tree = ET.ElementTree(self._geometry_file)
        tree.write("geometry.xml", xml_declaration=True,
                             encoding='utf-8', method="xml")
