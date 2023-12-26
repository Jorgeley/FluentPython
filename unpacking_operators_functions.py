# content is passed as tuple and attrs as dict
def tag(name, *content, cls=None, **attrs):
    print(type(content)) if content else None
    print(type(attrs)) if attrs else None
    if cls is not None:
        attrs["class"] = cls
    if attrs:
        attr_str = "".join(
            ' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items())
        )
    else:
        attr_str = ""
    if content:
        return "\n".join(
            "<%s%s>%s</%s>" % (name, attr_str, c, name) for c in content
        )
    else:
        return "<%s%s />" % (name, attr_str)


print(tag("br"))
print(tag("p", "hi"))
print(tag("p", "hi", "again"))  # 'hi', 'again' becomes *content as tuple
print(
    tag("p", "hi", id="bla")
)  # as 'id' is not a parameter in tag(), then becomes **attrs as dict


# * forces the function to accept only named args like 'b=99'
def only_named_args(b, *, a=1):
    print(f"b: {b}, a: {a}")
    pass


only_named_args(100, a=99)
only_named_args(b=101)
# only_named_args(99, 100)  # error since 2nd argument isn't named
