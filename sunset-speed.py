#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sunset-speed.py here.

at https://github.com/wilsonmar/python-samples/blob/main/sunset-speed.py

This program calculates how fast one would need to drive to experience a continuous sunset.

USAGE:
   chmod +x sunset-speed.py
   ./sunset-speed.py -deg 89
   ./sunset-speed.py -deg 40
"""

__last_change__ = "25-10-27 v001 new :sunset-speed.py"
__status__ = "working on macOS."


# math is a built-in library, so no pip install is needed.
import math
# the math library contains trigonomic functions such as cos() for cosigns.


def radians_cosign( radians_in ) -> float:
    """Calculate cosign for any angle in radians (just use math.cos directly)."""
    cos_value = math.cos(radians_in)
    print("Cosine of 1 radian:", cos_value)

def degrees_cosign( degrees_in ) -> float:
    """Calculate cosign for any degree."""
    angle_radians = math.radians(degrees_in)   # Convert 40 degrees to radians
    cos_value = math.cos(angle_radians)
    return cos_value
    # Since one full circle is: 360 degrees or 2π radians,
    # cosign(degrees) = angle in radians = angle in degrees * (π / 180)

def degrees_mph( degrees_in ):    
    """Print miles per hour from a given degree latitude."""
    cos_value = degrees_cosign( degrees_in )   
    mph = 1038 * cos_value
    print(f"Speed at {degrees_in:.4f} degrees for {mph:.2f} mph ({cos_value:.2f} radians)" \
          " around the world.")


if __name__ == '__main__':

    # If you were at 89.9 degrees North near a Pole, in the "land of the midnight sun",
    # you would be able to walk around all time zones quickly (at 1.81 mph).

    # But if you were at the equator, you would travel the circumference of the earth:
    # 40,075 km / 24 h ≈ <strong>1670 km/h (1038 mph)</strong> (the speed Earth rotates).
    # So the formula for speed is: v = 1038mph × cos(ϕ) where ϕ = latitude.
    # Denver, Colorado sits at around 40 degree latitude.
    # The cosign of 40 degrees at Denver, Colorado is 0.766, so <strong>1279 km/h (795 mph)</strong>.

    degrees_mph(89.9)
    degrees_mph(40)
