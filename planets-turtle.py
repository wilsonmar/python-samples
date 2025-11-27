#!/usr/bin/env python3

"""planets-turtle.py here.

at https://github.com/wilsonmar/python-samples/blob/main/planets-turtle.py

This illustrates a simple 2D map of planets around our solar system,
using object-oriented programming and the turtle graphics library built into Python.
to create planetary motion as shown by https://res.cloudinary.com/dcajqrroq/image/upload/v1764224322/planets-turtle-1484x1060_jzgzpx.png

Based on the Astronomy Animation code before modifications
of https://runestone.academy/ns/books/published/thinkcspy/Labs/astronomylab.html
using data from https://ssd.jpl.nasa.gov/planets/phys_par.html
adjusted to fit the screen:

   | Body | ? | ? | ? | ? | ? | color |
   |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
   | Sun  | 5000 | 10 | 5800 | - | - | yellow |
   | Pluto | 1 | 500 | 0.9 | 0 | .5 | orange |
   | MERCURY | 19.5 | 1000 | .25 | 0 | 2 | blue |
   | EARTH | 47.5 | 5000 | 0.3 | 0 | 2.0 | green |
   | MARS | 50 | 9000 | 0.5 | 0 | 1.63 | red |
   | JUPITER | 100 | 49000 | 0.7 | 0 | 1 | black |
   | Asteroid | 1 | 500 | 1.0 | 0 | .75 | cyan |

# Before running, on a Terminal
    # Create a folder:

    chmod +x planets-turtle.py
    ruff check planets-turtle.py
    uv run planets-turtle.py
    TODO: Add parameter to specify speed of full build of solar system image.

AFTER RUN:
    rm -rf .ruff_cache
"""
__last_change__ = "25-11-26 v002 + intro & ruff changes :planets-turtle.py"
__status__ = "WORKING on macOS"

# Built-in packages internal to Python:
import math
import turtle

class SolarSystem:
    """Define SolarSystem object."""

    def __init__(self, width, height):
        """Object constructor."""
        self.thesun = None
        self.planets = []
        self.ssturtle = turtle.Turtle()
        self.ssturtle.hideturtle()
        self.ssscreen = turtle.Screen()
        self.ssscreen.setworldcoordinates(-width/2.0,-height/2.0,width/2.0,height/2.0)
       # self.ssscreen.tracer(50)

    def add_planet(self, aplanet):
        """Add planet."""
        self.planets.append(aplanet)

    def add_sun(self, asun):
        """Add sun."""
        self.thesun = asun

    def show_planets(self):
        """Show planets."""
        for aplanet in self.planets:
            print(aplanet)

    def freeze(self):
        """Freeze it."""
        self.ssscreen.exitonclick()

    def move_planets(self):
        """Move planets."""
        gravity = .1
        dt = .001

        for p in self.planets:
           p.move_to(p.get_xpos() + dt * p.get_xvel(), p.get_ypos() + dt * p.get_yvel())

           rx = self.thesun.get_xpos() - p.get_xpos()
           ry = self.thesun.get_ypos() - p.get_ypos()
           r = math.sqrt(rx**2 + ry**2)

           accx = gravity * self.thesun.get_mass()*rx/r**3
           accy = gravity * self.thesun.get_mass()*ry/r**3

           p.set_xvel(p.get_xvel() + dt * accx)

           p.set_yvel(p.get_yvel() + dt * accy)

class Sun:
   """Define Sun object."""

   def __init__(self, iname, irad, im, itemp):
       self.name = iname
       self.radius = irad
       self.mass = im
       self.temp = itemp
       self.x = 0
       self.y = 0

       self.sturtle = turtle.Turtle()
       self.sturtle.shape("circle")
       self.sturtle.color("yellow")

   def get_name(self):
       """Get Name."""
       return self.name

   def get_radius(self):
       """Get Radius."""
       return self.radius

   def get_mass(self):
       """Get Mass."""
       return self.mass

   def get_temperature(self):
       """Get Temperature."""
       return self.temp

   def get_volume(self):
       """Get Volume."""
       v = 4.0/3 * math.pi * self.radius**3
       return v

   def get_surface_area(self):
       """Get SurfaceArea."""
       sa = 4.0 * math.pi * self.radius**2
       return sa

   def get_density(self):
       """Get Density."""
       d = self.mass / self.get_volume()
       return d

   def set_name(self, newname):
       """Set Name."""
       self.name = newname

   def __str__(self):
       """Set self."""
       return self.name

   def get_xpos(self):
       """Get XPos."""
       return self.x

   def get_ypos(self):
       """Get YPos."""
       return self.y

class Planet:
   """Define Planet object."""

   def __init__(self, iname, irad, im, idist, ivx, ivy, ic):
       self.name = iname
       self.radius = irad
       self.mass = im
       self.distance = idist
       self.x = idist
       self.y = 0
       self.velx = ivx
       self.vely = ivy
       self.color = ic

       self.pturtle = turtle.Turtle()
       #self.pturtle.speed('fast')
       self.pturtle.up()
       self.pturtle.color(self.color)
       self.pturtle.shape("circle")
       self.pturtle.goto(self.x,self.y)
       self.pturtle.down()

   def get_name(self):
       """Get Name."""
       return self.name

   def get_radius(self):
       """Get Radius."""
       return self.radius

   def get_mass(self):
       """Get Mass."""
       return self.mass

   def get_distance(self):
       """Get Distance."""
       return self.distance

   def get_volume(self):
       """Get Volume."""
       v = 4.0/3 * math.pi * self.radius**3
       return v

   def get_surface_area(self):
       """Get Surface Area."""
       sa = 4.0 * math.pi * self.radius**2
       return sa

   def get_density(self):
       """Get Density."""
       d = self.mass / self.get_volume()
       return d

   def set_name(self, newname):
       """Show it."""
       self.name = newname

   def show(self):
       """Show it."""
       print(self.name)

   def __str__(self):
       """Self name."""
       return self.name

   def move_to(self, newx, newy):
       """Move to."""
       self.x = newx
       self.y = newy
       self.pturtle.goto(newx, newy)

   def get_xpos(self):
       """Get xpos."""
       return self.x

   def get_ypos(self):
       """Get ypos."""
       return self.y

   def get_xvel(self):
       """Get xvel."""
       return self.velx

   def get_yvel(self):
       """Get yvel."""
       return self.vely

   def set_xvel(self, newvx):
       """Set xvel."""
       self.velx = newvx

   def set_yvel(self, newvy):
       """Set yvel."""
       self.vely = newvy


def create_ss_and_animate():
   """Create Solar System and animate."""
   ss = SolarSystem(2,2)

   sun = Sun("SUN", 5000, 10, 5800)
   ss.add_sun(sun)

   m = Planet("MERCURY", 19.5, 1000, .25, 0, 2, "blue")
   ss.add_planet(m)

   m = Planet("EARTH", 47.5, 5000, 0.3, 0, 2.0, "green")
   ss.add_planet(m)

   m = Planet("MARS", 50, 9000, 0.5, 0, 1.63, "red")
   ss.add_planet(m)

   m = Planet("JUPITER", 100, 49000, 0.7, 0, 1, "black")
   ss.add_planet(m)

   m = Planet("Pluto", 1, 500, 0.9, 0, .5, "orange")
   ss.add_planet(m)

   m = Planet("Asteroid", 1, 500, 1.0, 0, .75, "cyan")
   ss.add_planet(m)

   num_time_periods = 10000
   for amove in range(num_time_periods):
        ss.move_planets()

   ss.freeze()

create_ss_and_animate()
