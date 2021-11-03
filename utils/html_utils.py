
def tag(tabs, element, add_backslash, add_newline, **kwargs):
    add_tabs = '\t' * tabs
    html = f"""{add_tabs}<{element}"""
    if kwargs:
        html += ' '
        for i, key in enumerate(list(kwargs)):
            if i == len(kwargs) - 1:
                space = ''
            else:
                space = ' '
            if key == 'cls':
                html += f'class="{kwargs[key]}"' + space
            else:
                html += f'{key}="{kwargs[key]}"' + space
    if add_newline:
        n = '\n'
    else:
        n = ''
    if add_backslash:
        html += """ />""" + n
    else:
        html += """>""" + n
    return html


def tag_close(tabs, element, add_newline=True):
    if add_newline:
        n = '\n'
    else:
        n = ''
    add_tabs = '\t' * tabs
    return f"""{add_tabs}</{element}>""" + n


def tag_one_line(tabs, element, innerHTML, add_new_line, **kwargs):
    html = tag(tabs, element, False, False, **kwargs)
    html += str(innerHTML)
    html += tag_close(0, element, add_newline=add_new_line)
    return html


def tags_from_list(elements_list):
    html = ''
    for i in elements_list:
        args = i[:4]
        kwargs = i[4]
        html += tag(*args, **kwargs)
    return html


def tags_close_from_list(elements_list):
    close_list = [i[:2] for i in reversed(elements_list)]
    html = ''
    for i in close_list:
        html += tag_close(*i)
    return html






