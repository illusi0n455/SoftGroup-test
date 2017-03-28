import html


def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s


def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s


def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s


def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s


functions = {"p": html_p, "b": html_b, "i": html_i, "u": html_u}


def writer(tags):
    def decorator(func):
        def decorated(string):
            for i in tags:
                if i in functions:
                    string = functions[i](string)
            return func(string)

        return decorated

    return decorator


@writer('bpx')
def html_printer(s: str) -> str:
    return html.escape(s)

text = "I'll give you +++ cash for this -> stuff."
print(html_printer(text))
