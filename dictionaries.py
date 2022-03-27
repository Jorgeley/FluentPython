d1 = {'x': 'xxxx', 'y': 'yyyy'}
print(d1.get('x'))  # obviously
print(d1.get('w'))  # returns None, obviously
print(d1.get('w', 'N/A'))  # now we provide a default return
# print(d1['w'])  # raise KeyError


#  extending 'dict' to enforce string keys
class StrKeyDict0(dict):
    def __missing__(self, key):
        print("called __missing__()")
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    #  overwriting 'get()' to enforce 'gettitem()'
    def get(self, key, default='N/A'):
        print("called get()")
        try:  # __missing__ is only called by __getitem__(), i.e.: d2[3]
            return self[key]  # so, we enforce the dict[key] notation to activate __missing__()
        except KeyError:
            return default

    def __contains__(self, key):
        print("called __contains__()")
        return key in self.keys() or str(key) in self.keys()

d2 = StrKeyDict0({1: 1111, 2: 2222, 'z': 'zzzz'})
print(d2.get(1))  # calls 'get()'
print(d2[1])  # calls 'getitem()'
print(d2.get(2))
print(d2[2])
print(d2.get(3))  # calls 'get()' then '__missing__()'
print(4 in d2)  # calls '__contains__()'

