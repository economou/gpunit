import sys
import getopt
from math import sqrt
# Test code borrowed from test_hermite0.py.

from amuse.support.units import nbody_system
from amuse.support.units import units
from amuse.community.ph4.interface import ph4
from amuse.support.codes.core import is_mpd_running
from amuse.ext.plummer import MakePlummerModel
from amuse.ext.salpeter import new_salpeter_mass_distribution

number_of_stars = 1000
n_workers = 1

#Create Conversion Object
convert_nbody = nbody_system.nbody_to_si(
    1|units.MSun,
    1|units.Mpc
    )

#Initialize the Particles
particles = MakePlummerModel(
    number_of_stars,
    convert_nbody = convert_nbody
    ).result

#Create List of Masses
scaled_mass = new_salpeter_mass_distribution(number_of_stars)

#Set Particles Mass list to Salpeter Mass
particles.mass = scaled_mass

#Create Gravity Evolution
gravity = ph4(number_of_workers = n_workers, convert_nbody = convert_nbody)
gravity.initialize_code()
gravity.parameters.set_defaults()

#Adding Particles to Gravity and committing them to do initial calcultions
gravity.particles.add_particles(particles)
gravity.commit_particles()
