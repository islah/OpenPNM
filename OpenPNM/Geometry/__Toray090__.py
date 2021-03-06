"""
module __Toray090__: Subclass of GenericGeometry for a standard Toray TGPH090
gas diffusion layer.s
===============================================================================

.. warning:: The classes of this module should be loaded through the 'Geometry.__init__.py' file.

"""

from OpenPNM.Geometry import models as gm
from OpenPNM.Geometry import GenericGeometry

class Toray090(GenericGeometry):
    r"""
    Toray090 subclass of GenericGeometry

    """

    def __init__(self, **kwargs):
        r"""
        Initialize
        """
        super(Toray090,self).__init__(**kwargs)
        self._generate()

    def _generate(self):
        r'''
        '''
        self.add_model(propname='pore.seed',
                       model=gm.pore_misc.random,
                       num_range=[0,0.95],
                       seed=self._seed,
                       regen_mode='constant')
        self.add_model(propname='throat.seed',
                       model=gm.throat_misc.neighbor,
                       pore_prop='pore.seed',
                       mode='min')
        self.add_model(propname='pore.diameter',
                       model=gm.pore_diameter.sphere,
                       psd_name='weibull_min',
                       psd_shape=2.77,
                       psd_loc=6.9e-7,
                       psd_scale=9.8e-6,
                       psd_offset=10e-6)
        self.add_model(propname='pore.area',
                       model=gm.pore_area.spherical)
        self.add_model(propname='pore.volume',
                       model=gm.pore_volume.sphere)
        self.add_model(propname='throat.diameter',
                       model=gm.throat_diameter.cylinder,
                       tsd_name='weibull_min',
                       tsd_shape=2.77,
                       tsd_loc=6.9e-7,
                       tsd_scale=9.8e-6,
                       tsd_offset=10e-6)
        self.add_model(propname='throat.length',
                       model=gm.throat_length.straight)
        self.add_model(propname='throat.volume',
                       model=gm.throat_volume.cylinder)
        self.add_model(propname='throat.area',
                       model=gm.throat_area.cylinder)
        self.add_model(propname='throat.surface_area',
                       model=gm.throat_surface_area.cylinder)

if __name__ == '__main__':
    import OpenPNM
    pn = OpenPNM.Network.TestNet()
    pass
