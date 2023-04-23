from typing import List, Dict, Optional

from .mvcapi import MvcApi
from .provider import Provider, BroadcastResult
from ..constants import Chain


class Service:

    def __init__(self, chain: Optional[Chain] = None, provider: Optional[Provider] = None):
        if provider:
            self.provider = provider
        else:
            chain = chain or Chain.MAIN
            self.provider = MvcApi(chain=chain)
        self.chain = self.provider.chain

    def get_unspents(self, **kwargs) -> List[Dict]:
        """kwargs will pass the following at least
        {
            'private_keys': List[mvclib.keys.PrivateKey],
        }
        :returns: unspents in dict format refers to mvclib.transaction.unspent.Unspent
        """
        return self.provider.get_unspents(**kwargs)

    def get_balance(self, **kwargs) -> int:
        """kwargs will pass the following at least
        {
            'private_keys': List[mvclib.keys.PrivateKey],
        }
        :returns: balance in satoshi
        """
        return self.provider.get_balance(**kwargs)

    def broadcast(self, raw: str) -> BroadcastResult:
        """
        :returns: (True, txid) or (False, error_message)
        """
        return self.provider.broadcast(raw)  # pragma: no cover
