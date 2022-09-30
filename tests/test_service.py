from mvclib.constants import Chain
from mvclib.service.metasv import MetaSV


def test_metasv():
    service = MetaSV(chain=Chain.TEST)
    address = 'n27R7XNdewipj7hQct4bt6po1nsbVgVJGu'
    unspents = service.get_unspents(address=address)
    balance = service.get_balance(address=address)
    assert sum([unspent['satoshi'] for unspent in unspents]) == balance
