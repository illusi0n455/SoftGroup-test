import string


def filer_func(emails):
    emails = list(filter(lambda x: set(x).issubset(allowed) and x.count('@') == 1
                         and x.find('.', x.find('@')) - x.find('@') - 1 > 0
                         and len(''.join(x.split('.')[1:])) > 2, emails))
    return emails


allowed = set(string.ascii_letters + string.digits + '_@.')
emails = ['abc@gmail.com.ua', '*@ank.com', '_ny@us.gov.us', 'z@b.kk']
print(filer_func(emails))
