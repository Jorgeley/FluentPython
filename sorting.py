from operator import itemgetter, attrgetter

# sorting list of tuples by one specific value within the tuple
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
# itemgetter does exactly what is says: gets an item
print(
    itemgetter(1)(  # BR (from the result bellow)
        itemgetter(4)(metro_data)  # 'Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)
    ),
    "\n"
)
# can also be used with multiple indexes
print(
    itemgetter(1, 0)(  # country code - city
        metro_data[0]
    ),
    "\n"
)

for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
print("sorted by country code\n")

for city in sorted(metro_data, key=itemgetter(3)):
    print(city)
print("sorted by latitude")

