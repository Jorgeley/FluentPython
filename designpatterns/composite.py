import json
from abc import ABC, abstractmethod


class ItemMenuInterface(ABC):

    @abstractmethod
    def get_items(self) -> []:
        raise NotImplementedError("implement get_items()")


class ExploreMenu(ItemMenuInterface):

    class Query1Menu(ItemMenuInterface):

        def get_items(self) -> [ItemMenuInterface]:
            return [
                "Query1",
                [
                    "item 1",
                    "item 2"
                ]
            ]

    class Query2Menu(ItemMenuInterface):

        def get_items(self) -> [ItemMenuInterface]:
            return [
                "Query2",
                [
                    "item 1",
                    "item 2"
                ]
            ]

    def get_items(self) -> [ItemMenuInterface]:
        return [
            "Explore",
            self.Query1Menu().get_items(),
            self.Query2Menu().get_items()
        ]


print(json.dumps(ExploreMenu().get_items()))