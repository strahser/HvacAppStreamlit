import collections
def to_list(element)->list:
    if isinstance(element, list):
        res = element
    else:
        res = [element]
    return res


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def Flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in Flatten(i)]
    else:
        return [x]
    
