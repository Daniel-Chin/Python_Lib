from __future__ import annotations

from typing import Tuple, Union, Dict

class BaseLossTree:
    __slots__ = ['name', 'children']
    def __init__(self) -> None:
        self.name = (
            self.__class__.__name__.lower()
            .replace('loss', '')
            .replace('_', '')
        )
        self.children: Dict[
            str, Union[BaseLossTree, float], 
        ] = {}
        for child in self.childrenTypes():
            if isinstance(child, type) and issubclass(child, BaseLossTree):
                instance = child()
                key, value = instance.name, instance
            else:
                key, value = child, None
            self.children[key] = value
    
    def __getattr__(self, __name):
        return self.children[__name]
    
    def __setattr__(self, __name: str, __value) -> None:
        if __name in self.__slots__:
            super().__setattr__(__name, __value)
        else:
            self.children[__name] = __value
    
    def __repr__(self):
        buf = []
        for key, value in self.children.items():
            if issubclass(value.__class__, BaseLossTree):
                buf.append(repr(value))
            else:
                try:
                    value = value.item()
                except AttributeError:
                    pass
                buf.append(f'{key} loss={value}')
        return f'<{self.name}: ' + ' & '.join(buf) + '>'

    def childrenTypes(self) -> Tuple[Union[BaseLossTree, str]]:
        # To override
        raise NotImplemented

def demo():
    class VaeLoss(BaseLossTree):
        def childrenTypes(self) -> Tuple[BaseLossTree]:
            return ('reconstruct', 'kld')
    class PredictLoss(BaseLossTree):
        def childrenTypes(self) -> Tuple[BaseLossTree]:
            return ('z', 'image')
    class VrnnLoss(BaseLossTree):
        def childrenTypes(self) -> Tuple[BaseLossTree]:
            return (PredictLoss, 'kld')
    class TotalLoss(BaseLossTree):
        def childrenTypes(self) -> Tuple[BaseLossTree]:
            return (VaeLoss, VrnnLoss)

    totalLoss = TotalLoss()
    totalLoss.vae.reconstruct = 1
    totalLoss.vae.kld = 2
    totalLoss.vrnn.predict.z = 3
    totalLoss.vrnn.predict.image = 4
    totalLoss.vrnn.kld = 5

    print(totalLoss)

if __name__ == '__main__':
    demo()
