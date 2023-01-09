from states.user_states import UserInfoState as U


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
        if U.language_code == 'ru':
            return 'Северный'
        elif U.language_code == 'en':
            return 'North'
        elif U.language_code == 'fr':
            return 'Nord'
        elif U.language_code == 'de':
            return 'Nordisch'
    elif wind in cv:
        if U.language_code == 'ru':
            return 'Северо-Восточный'
        elif U.language_code == 'en':
            return 'North-East'
        elif U.language_code == 'fr':
            return 'Nord-Est'
        elif U.language_code == 'de':
            return 'Nordosten'
    elif wind in v:
        if U.language_code == 'ru':
            return 'Восточный'
        elif U.language_code == 'en':
            return 'East'
        elif U.language_code == 'fr':
            return 'Est'
        elif U.language_code == 'de':
            return 'Ost'
    elif wind in yv:
        if U.language_code == 'ru':
            return 'Юго-Восточный'
        elif U.language_code == 'en':
            return 'South-East'
        elif U.language_code == 'fr':
            return 'Sud-Est'
        elif U.language_code == 'de':
            return 'Südöstlich'
    elif wind in y:
        if U.language_code == 'ru':
            return 'Южный'
        elif U.language_code == 'en':
            return 'South'
        elif U.language_code == 'fr':
            return 'Sud'
        elif U.language_code == 'de':
            return 'Südlich'
    elif wind in yz:
        if U.language_code == 'ru':
            return 'Юго-Западный'
        elif U.language_code == 'en':
            return 'South-West'
        elif U.language_code == 'fr':
            return 'Sud-Ouest'
        elif U.language_code == 'de':
            return 'Südwestlich'
    elif wind in z:
        if U.language_code == 'ru':
            return 'Западный'
        elif U.language_code == 'en':
            return 'West'
        elif U.language_code == 'fr':
            return 'Ouest'
        elif U.language_code == 'de':
            return 'Westlich'
    elif wind in cz:
        if U.language_code == 'ru':
            return 'Северо-Западный'
        elif U.language_code == 'en':
            return 'North-West'
        elif U.language_code == 'fr':
            return 'Nord-Ouest'
        elif U.language_code == 'de':
            return 'Nordwestlich'
