.. _getting_started:

###############################################################################
Getting Started with OpenPNM
###############################################################################
The OpenPNM framework is built upon 5 main objects, Networks, Geometries, Phases, Physics and Algorithms.  All of these objects are subclassed from the Python 'dictionary' or ``dict``, which is a data storage class similar to a *struct* in C or Matlab.  Using a ``dict`` means that multiple pieces of data can be stored on each object, and accessed by name (i.e. object_name['pore.diameter']) which provide easy and direct access to the numerical data.  Each OpenPNM object stores its own data, so the *Network* object stores topological information, *Geometries* stores pore and throat size related information, *Phases* stores the physical properties of the fluids and solids in the network, *Physics* stores pore-scale physics information, and *Algorithms* store the results of simulations and calculations.  A detailed discussion of the OpenPNM data storage scheme is provided :ref:`here<network>`.

The OpenPNM objects use ``dict`` as a starting point, but augment it by adding a variety of methods that work with the data stored in the dictionaries.  For instance, the basic ``dict`` class only has a few methods for reading and removing data from the dictionary, while an OpenPNM object has many additional methods related to pore network modeling, such as querying the number of pores in the network.  

===============================================================================
Main Modules
===============================================================================

1 `Network`_: The Network object is the main *controller* object for the framework.  It contains all the topological information about the **Network**, as well as methods for querying and manipulating the topology. 

2 `Geometry`_: Geometry objects manage the pore-scale geometrical properties of the Network such as pore volume and throat diameter.  A simulation may have multiple Geometry objects depending on the problem being modeled.  For instance, a stratified material may have a separate Geometry object for each layer if the pore and throat sizes differ between them.  

3 `Phases`_: Phase objects contain information about the thermo-physical properties of the liquids, gases, and solids required in the simulation.  For instance, a Phase object for water would possess its temperature, as well as models for calculating its viscosity as a function of temperature (and any other relevant properties).

4 `Physics`_: Physics objects contain methods for calculating pores physical and conductance properties which use values from the *Phase* and *Geometry* objectives. For instance, the hydraulic conductance of a throat requires knowing the throat diameter and length, as well as the fluid viscosity.  

5 `Algorithms`_: This module is the home of the actual algorithms that use the network properties defined by the above modules.  OpenPNM ships with a good assortment of standard algorithms, but is meant to be extended by users adding custom algorithms.

The 5 objects listed above interact with each other to create a 'simulation'.  When viewed schematically, these objects interact as shown in the following figure:

.. figure:: ../ObjectHierarchy.png
    :width: 100%
    :align: center
    :alt: alternate text
    :figclass: align-left

    *Object relationship diagram for an arbitrary simulation with 3 Geometries, 2 Phases, 3 Physics and 3 Algorithms.  These numbers are entirely dependent on the model.*

	
The vertical positioning of the blocks in this image shows that Networks, Phases and Algorithms span the entire set of pores (and throats) in the Network, while Geometry and Physics objects are assigned to arbitrary sections of pores (and throats).  The color scheme represents the fact that Geometries are directly connected to a Network object, and Physics objects are directly connected to a Phase object.  With this picture in mind, the relationships between objects and the flow of responsibility in the simulation as outlined below will be more clear.  

===============================================================================
Network
===============================================================================
A Cubic Network can be created with:

>>> import OpenPNM
>>> pn = OpenPNM.Network.Cubic(shape=[3,3,3],spacing=10,name='net1')
>>> print(pn)
------------------------------------------------------------
OpenPNM.Network.Cubic: 	net1
------------------------------------------------------------
#     Properties                          Valid Values
------------------------------------------------------------
1     pore.coords                            27 / 27   
2     pore.index                             27 / 27   
3     pore.subscript                         27 / 27   
4     throat.conns                           54 / 54   
------------------------------------------------------------
#     Labels                              Assigned Locations
------------------------------------------------------------
1     pore.all                            27        
2     pore.back                           9         
3     pore.bottom                         9         
4     pore.front                          9         
5     pore.internal                       27        
6     pore.left                           9         
7     pore.right                          9         
8     pore.top                            9         
9     throat.all                          54        
------------------------------------------------------------

As can be seen from the print-out of the Network, 'net1' has 27 pores with 54 throats, 3 'properties' and 9 'labels'.  The labels were applied to this Network by the Cubic generator, and they have no special meaning but are useful (with the exception of 'all', but more on this later).  The 'pore.coords' and 'throat.conns' properties, however, are absolutely essential to the network as these define the topology and spatial arrangement of the pores and throats.  ('pore.index' is non-essential).  

The Network object is explained further in the :ref:`Network Documentation<network>`.

===============================================================================
Geometry
===============================================================================
You'll notice that the Network object has no *pore-scale* geometric information such as 'size' and 'volume'.  This type of data is managed by the Geometry objects.  A standard 'stick and ball' Geometry object can be created with:

>>> geom = OpenPNM.Geometry.Stick_and_Ball(network=pn,pores=pn.pores('all'),throats=pn.throats('all'))
>>> print(geom)
------------------------------------------------------------
#     Properties                          Valid Values
------------------------------------------------------------
1     pore.area                              27 / 27   
2     pore.diameter                          27 / 27   
3     pore.seed                              27 / 27   
4     pore.volume                            27 / 27   
5     throat.area                            54 / 54   
6     throat.diameter                        54 / 54   
7     throat.length                          54 / 54   
8    throat.seed                            54 / 54   
9    throat.surface_area                    54 / 54   
10    throat.volume                          54 / 54   
------------------------------------------------------------
#     Labels                              Assigned Locations
------------------------------------------------------------
1     pore.all                            27        
2     throat.all                          54        
------------------------------------------------------------

As can be seen this Geometry object contains all the expected pore-scale geometric information.  The 'stick_and_ball' subclass is provided with OpenPNM and already contains all the pore scale models pre-selected.  Further details on creating a custom Geometry object are provided in the :ref:`Geometry Documentation<geometry>`.

The instantiation of this object has a few requirements that should be pointed out.  Firstly, it must receive a Network object to which it is to be associated.  Secondly, it must receive a list of pores and throats where it is to apply.  In the above example, ``geom`` applies to *all* pores and throats, but it possible and likely that multiple Geometry objects will be applied to the same Network.  

===============================================================================
Phases
===============================================================================
In any pore network simulation there are usually several fluids whose transport processes are to be simulated.  The thermo-physical properties of each of the fluids are managed by a Phase object:

>>> air = OpenPNM.Phases.Air(network=pn,name='air')
>>> print(air)
------------------------------------------------------------
#     Properties                          Valid Values
------------------------------------------------------------
1     pore.critical_pressure                 27 / 27   
2     pore.critical_temperature              27 / 27   
3     pore.diffusivity                       27 / 27   
4     pore.molar_density                     27 / 27   
5     pore.molecular_weight                  27 / 27   
6     pore.pressure                          27 / 27   
7     pore.temperature                       27 / 27   
8     pore.viscosity                         27 / 27   
------------------------------------------------------------
#     Labels                              Assigned Locations
------------------------------------------------------------
1     pore.all                            27        
2     throat.all                          54        
------------------------------------------------------------

The *Air* subclass is included with OpenPNM and contains all necessary models for calculating each property as a function of the conditions.  Building a custom Phase to represent other fluids is outlined in the :ref:`Phases Documentation<phases>`.

Notice that pores and throats were *not* sent to the GenericPhase constructor.  This is because *Phases* exist everywhere.  This might seem counterintuitive in a multiphase simulation where one phase displaces another, but it is much easier to calculate the *Phase* properties everywhere, and separately track where each phase is present and in what amount.  

===============================================================================
Physics
===============================================================================
When performing a pore network simulation, one of the main aims is to combine phase properties with geometry sizes to estimate the behavior of a fluid as it moves through the pore space.  The pore-scale physics models required for this are managed by Physics objects:

>>> phys = OpenPNM.Physics.Standard(network=pn,phase=air,pores=pn.pores('all'),throats=pn.throats('all'))
>>> print(phys)
------------------------------------------------------------
OpenPNM.Physics.Standard: 	Standard_SzZPQ
------------------------------------------------------------
#     Properties                          Valid Values
------------------------------------------------------------
1     throat.diffusive_conductance           54 / 54   
2     throat.hydraulic_conductance           54 / 54   
------------------------------------------------------------
#     Labels                              Assigned Locations
------------------------------------------------------------
1     pore.all                            27        
2     throat.all                          54        
------------------------------------------------------------

The ``Standard`` Physics object is a special subclass included with OpenPNM.  It uses the 'standard' pore-scale physics models.  Further details on creating custom Physics objects are provided in the :ref:`Physics Documentation<physics>`.

The Physics object requires several arguments in its instantiation.  Like all other objects, it requires a Network object with which it is to be associated.  It also requires the Fluid to which it applies.  This enables it to ask 'air' for viscosity values when calculating hydraulic conductance.  Finally, it requires the pores and/or throats where the Physics should apply.  Notice that no Geometry object is sent as an argument, yet all pore scale physics models will clearly require geometric information.  Instead of associating a Physics directly with a Geometry object, a Physics object is applied to pores and throats independently.  When geometric data is required, the Physics object asks the Network object for the values, and the Network then retrieves them from the appropriate Geometry objects.  

===============================================================================
Algorithms
===============================================================================
The final step in performing a pore network simulation is to run some algorithms to model transport processes in the network.  OpenPNM comes with numerous algorithms, such as ``FickianDiffusion`` for modeling diffusion mass transport:

>>> alg = OpenPNM.Algorithms.FickianDiffusion(network=pn, phase=air)
>>> Ps1 = pn.pores(labels=['top'])
>>> alg.set_boundary_conditions(bctype='Dirichlet', bcvalue=0.6, pores=Ps1)
>>> Ps2 = pn.pores(labels=['bottom'])
>>> alg.set_boundary_conditions(bctype='Dirichlet', bcvalue=0.4, pores=Ps2)
>>> alg.run(phase=air)
>>> print(alg)
------------------------------------------------------------
OpenPNM.Algorithms.FickianDiffusion: 	FickianDiffusion_kr2XO
------------------------------------------------------------
#     Properties                          Valid Values
------------------------------------------------------------
1     pore.air_bcval_Dirichlet               18 / 27   
2     pore.air_mole_fraction                 27 / 27   
3     throat.conductance                     54 / 54   
------------------------------------------------------------
#     Labels                              Assigned Locations
------------------------------------------------------------
1     pore.air_Dirichlet                  18        
2     pore.all                            27        
3     throat.all                          54        
------------------------------------------------------------

As can be seen in the above print-out, the Algorithm object contains some boundary condition related properties and labels, but more importantly, it contains 'pore.air_mole_fraction' which is the result of the ``FickianAlgorithm`` simulation.  Each algorithm in OpenPNM will produce a different result with a different name, and this data stays encapsulated in the Algorithm object unless otherwise desired.  For instance, if the 'pore.air_mole_fraction' data is required in another algorithm, then it is necessary to write it to 'air':

>>> air['pore.air_mole_fraction'] = alg['pore.air_mole_fraction']

More detailed information about Algorithm objects can be found in the :ref:`Algorithm Documentation<algorithms>`








