

def dict_merge(dict_1, dict_2):
    for k, v in dict_2.items():
        if k in dict_1 and isinstance(dict_1[k], dict) and isinstance(v, dict):
            dict_merge(dict_1[k], v)
        else:
            dict_1[k] = v
    return dict_1

def rename_dictionary(old_dict:dict,replace_dict:dict)->dict:
    """replace keys in dictionary by another dictinory
    rerurn dict


    Args:
        old_dict (dict): existing dictionary
        replace_dict (dict): _description_

    Returns:
        dict: _description_
    """
    new_dict = {}
    for key,value in zip(old_dict.keys(),old_dict.values()):
        if key in replace_dict.keys():
            new_key = replace_dict[key]
            new_dict[new_key] = old_dict[key]
        else:
            new_dict[key] = old_dict[key]
    return new_dict


def join_dict(dicts:dict)->dict:
    hb_dict = {key: val for d in dicts for key, val in d.items()}
    return hb_dict
