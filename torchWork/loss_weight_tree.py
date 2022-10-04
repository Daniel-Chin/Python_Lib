from __future__ import annotations

from typing import List, Optional

class LossWeightTree:
    def __init__(
        self, name: str, weight: float, 
        children: Optional[List[LossWeightTree]], 
    ) -> None:
        self.name = name
        self.weight = weight
        self.children = children
