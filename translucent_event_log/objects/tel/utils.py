
def tel_set_enabled(tel):

    '''
    read and set enabled attribute in tel object

    :param tel: tel object without enabled attribute
    :return: tel object with enabled attribute
    '''

    for trace in tel:
        for event in trace:
            if event['enabled'] != 'set()':
                en_list = event['enabled'][1:-1].split(',')
                en = set()
                for i in en_list:
                    #activity name should be alphabet, digit
                    if not (i[0].isdigit() or i[0].isalpha()) :
                        i = i[1:]
                    if not (i[0].isdigit() or i[0].isalpha()):
                        i = i[1:]
                    if not (i[-1].isdigit() or i[-1].isalpha()):
                        i = i[:-1]
                    en.add(i)
                event.set_enabled(frozenset(en))
            else:
                event.set_enabled(frozenset())

    return tel