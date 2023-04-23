from mvclib.constants import Chain
from mvclib.keys import Key
from mvclib.script.type import P2pkScriptType
from mvclib.service import MvcApi
from mvclib.wallet import Wallet


def test_chain_provider():
    w = Wallet()
    assert w.chain == Chain.MAIN
    assert w.provider is None

    w = Wallet(chain=Chain.TEST)
    assert w.chain == Chain.TEST
    assert w.provider is None

    w = Wallet(provider=MvcApi(Chain.TEST))
    assert w.chain == Chain.TEST
    assert isinstance(w.provider, MvcApi)
    assert w.provider.chain == Chain.TEST


def test():
    p1 = Key('cT6HWfEFaYtaZiPqaBr7CrN8z346ns13G6Mo6sgWZN82XuibXbzJ')
    p2 = Key('cQKZWZsXGX1MTwmmYW9FYQdAJ9wwnQPo9gEDARSCHewuRxyHFFRo')

    w1 = Wallet(chain=Chain.TEST).add_key(p1).add_key(p2)
    w2 = Wallet(chain=Chain.TEST).add_keys([p1, p2])
    w3 = Wallet(keys=[p1, p2], chain=Chain.TEST)

    assert w1.get_keys() == w2.get_keys()
    assert w1.get_keys() == w3.get_keys()

    assert w1.get_unspents() == []
    assert w1.get_balance() == 0

    w1.get_unspents(refresh=True)
    assert w1.get_balance() == w1.get_balance(refresh=True)

    w2.get_unspents(refresh=True)
    assert w2.get_balance() == w2.get_balance(refresh=True)

    has_p2pk = False
    for unspent in w2.get_unspents():
        if unspent.script_type == P2pkScriptType():
            has_p2pk = True
            break
    if has_p2pk:
        assert w1.get_balance() < w2.get_balance()
    else:
        assert w1.get_balance() == w2.get_balance()
