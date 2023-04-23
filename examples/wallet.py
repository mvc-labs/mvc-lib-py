from mvclib import WalletLite
from mvclib.constants import Chain
from mvclib.hd import derive_xprv_from_mnemonic, derive_xprvs_from_mnemonic

mnemonic = 'purchase upon spell inch cool remove depart amateur glass wheel seek royal'
chain = Chain.TEST

xprv = derive_xprv_from_mnemonic(mnemonic=mnemonic, chain=chain)
xkeys = derive_xprvs_from_mnemonic(mnemonic=mnemonic, chain=chain, index_start=0, index_end=3)
for xkey in xkeys:
    print(xkey.address())

w = WalletLite(xprv, token='', client_key='')  # <-- set your token or client key here

print('-------- refresh unspents --------')
for unspent in w.get_unspents(refresh=True):
    print(unspent)

print('-------- send a transaction --------')
t = w.create_transaction(outputs=[('myDKFHUEbh6JiZ9WdEVhKEHiCL9foMiBkZ', 500001)])
print(t.broadcast())

print('-------- used unspent will be removed from wallet automatically --------')
for unspent in w.get_unspents():
    print(unspent)

print('-------- refresh unspents agin --------')
for unspent in w.get_unspents(refresh=True):
    print(unspent)
