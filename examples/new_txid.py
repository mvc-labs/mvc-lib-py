from mvclib import Wallet, Key, Transaction
from mvclib.constants import Chain

key = Key('cVwfreZB3i8iv9JpdSStd9PWhZZGGJCFLS4rEKWfbkahibwhticA')

w = Wallet(chain=Chain.TEST).add_key(key)
print(w.get_balance(refresh=True))

outputs = [('mqBuyzdHfD87VfgxaYeM9pex3sJn4ihYHY', 666)]
pushdatas = ['hello', b'world']
t: Transaction = w.create_transaction(outputs=outputs, pushdatas=pushdatas)
print(t.broadcast())
print(t.raw())
print(f'new txid - {t.new_txid()}')
