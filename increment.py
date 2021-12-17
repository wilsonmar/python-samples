# increment.py

"""This increments (creates a new) serial number with every invocation of the class."""
# STATUS: Not working. See FIXME tag below.

# from https://app.pluralsight.com/course-player?clipId=bf34ecab-aa3e-402b-961d-53efb624b957

class ShippingContainer:   # Global scope

    # Class attributes here:
    next_serial = 1337  # IRL this would be obtained from a persistant database?

    def __init__(self, owner_code, contents):

    	# self. instance attributes:
        self.owner_code = owner_code
        self.contents = contents
        self.serial = ShippingContainer.next_serial

        # Class attributes:
        ShippingContainer.next_serial += 1   # increment

##############
print(f'Executing from ShippingContainer.next_serial={ShippingContainer.next_serial} :')
owner_code="ESC"
contents='["Electronics"]'
print(f'owner_code={owner_code} contents={contents}')
#print(f'ShippingContainer.owner_code={ShippingContainer.owner_code}')
#print(f'ShippingContainer.contents={ShippingContainer.contents}')

# FIXTHIS: No incrementing:
c4 = ShippingContainer(owner_code, contents)
print(c4.serial)

"""
c1 = ShippingContainer.next_serial
print(c1)
c1 = ShippingContainer.next_serial
print(c1)

c3 = ShippingContainer("ESC", ["Pharmaceuticals"])
c4 = ShippingContainer("ESC", ["Pharmaceuticals"])
c5 = ShippingContainer("ESC", ["Pharmaceuticals"])
c6 = ShippingContainer("ESC", ["Noodles"])
"""