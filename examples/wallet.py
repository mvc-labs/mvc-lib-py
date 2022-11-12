from mvclib import WalletLite
from mvclib.constants import Chain
from mvclib.hd import derive_xprv_from_mnemonic, derive_xprvs_from_mnemonic
from mvclib.service import MetaSV

mnemonic = 'purchase upon spell inch cool remove depart amateur glass wheel seek royal'
path = "m/44'/10001'/0'"
chain = Chain.TEST

token = ''  # <-- your token here
provider = MetaSV(chain=chain, token=token)

xprv = derive_xprv_from_mnemonic(mnemonic=mnemonic, path=path, chain=chain)
xkeys = derive_xprvs_from_mnemonic(mnemonic=mnemonic, path=path, chain=chain, index_start=0, index_end=3)
for xkey in xkeys:
    print(xkey.address())

w = WalletLite(xprv)

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
