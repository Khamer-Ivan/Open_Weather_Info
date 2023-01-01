def wind_info(wind):
    c_1 = range(337, 380)
    c_2 = range(0, 22)
    cv = range(22, 67)
    v = range(67, 112)
    yv = range(112, 157)
    y = range(157, 202)
    yz = range(202, 247)
    z = range(247, 292)
    cz = range(292, 337)

    if wind in c_1 or wind in c_2:
        return 'Северный'
    elif wind in cv:
        return 'Северо-Восточный'
    elif wind in v:
        return 'Восточный'
    elif wind in yv:
        return 'Юго-Восточный'
    elif wind in y:
        return 'Южный'
    elif wind in yz:
        return 'Юго-Западный'
    elif wind in z:
        return 'Западный'
    elif wind in cz:
        return 'Северо-Западный'
