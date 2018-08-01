from abc import abstractmethod
from typing import (
    Dict,
    Type,
)

from p2p.peer import BasePeer
from p2p.protocol import _DecodedMsgType
from p2p.service import BaseService

from .managers import BaseRequestManager
from .requests import BaseRequest


class BaseRequestResponseHandler(BaseService):
    @property
    @abstractmethod
    def _managers(self) -> Dict[str, Type[BaseRequestManager[BasePeer, BaseRequest, _DecodedMsgType, _DecodedMsgType]]]:
        pass

    def __init__(self, peer: BasePeer) -> None:
        self._peer = peer

        super().__init__(peer.cancel_token)
        for attr, request_manager_cls in self._managers.items():
            if hasattr(self, attr):
                raise AttributeError(
                    "Unable to set manager on attribute `{0}` which is already "
                    "present on the class: {1}".format(attr, getattr(self, attr))
                )
            manager = request_manager_cls(self._peer, self.cancel_token)
            setattr(self, attr, manager)

    async def _run(self) -> None:
        for attr in self._managers.keys():
            manager = getattr(self, attr)
            self.run_child_service(manager)

        while not self.cancel_token.triggered:
            await self.sleep(0.01)

    async def _cleanup(self) -> None:
        pass
