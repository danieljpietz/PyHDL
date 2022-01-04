_reserved = "abs access after alias all and architecture array assert attribute begin block body buffer bus case " \
            "component configuration constant disconnect downto else elsif end entity exit file for function generate "\
            "generic group guarded if impure in inertial inout is label library linkage literal loop map mod nand new "\
            "next nor not null of on open or others out package port postponed procedure process pure range record " \
            "register reject return rol ror select severity signal shared sla sli sra srl subtype then to transport " \
            "type unaffected units until use variable wait when while with xnor xor".split(' ')


def check_name(name: str):
    if isinstance(name, str):
        if name.lower() in _reserved:
            raise NameError(f"Name {name} is a reserved keyword")
    else:
        raise TypeError (f"Unexpected type for symbol name. Expected str but found {type(name)}")

