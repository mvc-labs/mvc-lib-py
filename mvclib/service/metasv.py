import base64
import json
import random
import time
from contextlib import suppress
from typing import Optional, List, Dict, Union, Tuple

import requests

from .provider import Provider, BroadcastResult
from ..constants import Chain, METASV_TOKEN, METASV_CLIENT_KEY
from ..hash import sha256
from ..hd import Xprv, Xpub
from ..keys import Key


class MetaSV(Provider):  # pragma: no cover

    def __init__(self, chain: Chain = Chain.MAIN, url: Optional[str] = None, headers: Optional[Dict] = None,
                 timeout: Optional[int] = None, token: Optional[str] = None, client_key: Optional[str] = None):
        assert chain == Chain.TEST, 'MetaSV service now only supports Chain.TEST'
        self.url = url or 'https://api-mvc-testnet.metasv.com'
        super().__init__(chain, headers, timeout)
        self.token = token or METASV_TOKEN
        self.client_key = client_key or METASV_CLIENT_KEY

    def _get_unspents(self, address: str, flag: Optional[str] = None) -> Union[Dict, List[Dict]]:
        with suppress(Exception):
            params = {}
            if flag:
                params['flag'] = flag
            return self.get(url=f'{self.url}/address/{address}/utxo', params=params)
        return []

    def get_unspents(self, **kwargs) -> List[Dict]:
        try:
            address, _, _ = self.parse_kwargs(**kwargs)
            # paging
            paged_unspents: List[Dict] = self._get_unspents(address)
            total_unspents: List[Dict] = paged_unspents
            while paged_unspents:
                paged_unspents = self._get_unspents(address, paged_unspents[-1]['flag'])
                total_unspents.extend(paged_unspents or [])
            # parsing
            unspents: List[Dict] = []
            for item in total_unspents:
                unspent = {'txid': item['txid'], 'vout': item['outIndex'], 'satoshi': item['value'], 'height': item['height']}
                unspent.update(kwargs)
                unspents.append(unspent)
            return unspents
        except Exception as e:
            if kwargs.get('throw'):
                raise e
        return []

    def get_balance(self, **kwargs) -> int:
        try:
            address, _, _ = self.parse_kwargs(**kwargs)
            r: Dict = self.get(url=f'{self.url}/address/{address}/balance')
            return r.get('confirmed') + r.get('unconfirmed')
        except Exception as e:
            if kwargs.get('throw'):
                raise e
        return 0

    def broadcast(self, raw: str) -> BroadcastResult:
        propagated, message = False, ''
        try:
            data = json.dumps({'hex': raw})
            _r = requests.post(f'{self.url}/tx/broadcast', headers=self.headers, data=data, timeout=self.timeout)
            _r.raise_for_status()
            r = _r.json()
            assert r, f'empty response {r}'
            if r.get('txid'):
                propagated, message = True, r['txid']
            else:
                propagated, message = False, r.get('message')
        except Exception as e:
            message = message or str(e)
        return BroadcastResult(propagated, message)

    def parse_headers(self, path: str) -> Dict:
        if self.token:
            return {**self.headers, **{'Authorization': f'Bearer {self.token}', }}
        elif self.client_key:
            k = Key(self.client_key)
            timestamp = str(int(time.time() * 1000))
            nonce = ''.join(str(random.choice(range(10))) for _ in range(10))
            message = f'{path}_{timestamp}_{nonce}'.encode('utf-8')
            sig = base64.b64encode(k.sign(message=message, hasher=sha256))
            return {**self.headers, **{
                'MetaSV-Timestamp': timestamp, 'MetaSV-Nonce': nonce,
                'MetaSV-Client-Pubkey': k.public_key().hex(), 'MetaSV-Signature': sig,
            }}
        else:
            return self.headers

    @classmethod
    def _parse_xkey(cls, **kwargs) -> Tuple[Optional[Xpub], Optional[Xprv]]:
        """
        try to parse out (xpub, xprv) from kwargs
        """
        xprv: Xprv = kwargs.get('xprv') or None
        xpub: Xpub = kwargs.get('xpub') or (xprv.xpub() if xprv else None)
        return xpub, xprv

    def get_xpub_unspents(self, **kwargs) -> List[Dict]:
        assert self.token or self.client_key, 'MetaSV service requires a token or a client key'
        try:
            xpub, xprv = MetaSV._parse_xkey(**kwargs)
            path = f'/xpubLite/{xpub}/utxo'
            r: Dict = self.get(url=f'{self.url}{path}', headers=self.parse_headers(path))
            unspents: List[Dict] = []
            for item in r:
                unspent = {'txid': item['txid'], 'vout': item['txIndex'], 'satoshi': item['value'], 'height': item['height']}
                unspent.update(kwargs)
                if xprv:
                    # update private key
                    unspent.update({'private_keys': [xprv.ckd(item['addressType']).ckd(item['addressIndex']).private_key()]})
                unspents.append(unspent)
            return unspents
        except Exception as e:
            if kwargs.get('throw'):
                raise e
        return []

    def get_xpub_balance(self, **kwargs) -> int:
        assert self.token or self.client_key, 'MetaSV service requires a token or a client key'
        try:
            xpub, xprv = MetaSV._parse_xkey(**kwargs)
            path = f'/xpubLite/{xpub}/balance'
            r: Dict = self.get(url=f'{self.url}{path}', headers=self.parse_headers(path))
            return r.get('balance')
        except Exception as e:
            if kwargs.get('throw'):
                raise e
        return 0
