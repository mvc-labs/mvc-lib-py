from mvclib.constants import Chain
from mvclib.service import Service, MvcApi


def test_mvcapi():
    provider = MvcApi(chain=Chain.TEST)

    s = Service(provider=provider)
    assert s.chain == provider.chain

    address = 'n27R7XNdewipj7hQct4bt6po1nsbVgVJGu'
    unspents = provider.get_unspents(address=address)
    balance = provider.get_balance(address=address)
    assert sum([unspent['satoshi'] for unspent in unspents]) == balance
