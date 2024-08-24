from typing import Self

from src.domain.entities.payment import PaymentEntity

from src.domain.value_objects.uuid import UUIDValueObject

from src.domain.repositories.payment import IPaymentRepository


class _Node:
    def __init__(self, value: PaymentEntity):
        self.value: PaymentEntity = value
        self.left: Self = None
        self.right: Self = None


class _BinaryTree:
    def __init__(self):
        self.root: _Node = None

    def save(self, value: PaymentEntity):
        if self.root is None:
            self.root = _Node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value: PaymentEntity, current_node: _Node) -> None:
        if (
            value.id.convert_value_to_UUID()
            < current_node.value.id.convert_value_to_UUID()
        ):
            if current_node.left is None:
                current_node.left = _Node(value)
            else:
                self._insert(value, current_node.left)
        elif (
            value.id.convert_value_to_UUID()
            > current_node.value.id.convert_value_to_UUID()
        ):
            if current_node.right is None:
                current_node.right = _Node(value)
            else:
                self._insert(value, current_node.right)
        else:
            raise Exception("element already exists in tree")

    def find_by_id(self, uuid: UUIDValueObject) -> PaymentEntity:
        node: _Node = self._inorder_traversal(self.root, uuid)
        if node is None:
            return None
        return node.value

    def update(self, entity: PaymentEntity) -> None:
        node: _Node = self._inorder_traversal(self.root, entity.id)
        if node is None:
            raise Exception("element does not exists in tree")
        node.value = entity

    def _inorder_traversal(self, node: _Node, id: UUIDValueObject) -> _Node:
        if node is None:
            return None

        if node.value.id.convert_value_to_UUID() > id.convert_value_to_UUID():
            return self._inorder_traversal(node.left, id)
        elif node.value.id.convert_value_to_UUID() < id.convert_value_to_UUID():
            return self._inorder_traversal(node.right, id)
        else:
            return node


class FakePaymentRepository(IPaymentRepository):
    _instance: Self = None

    def __new__(cls, *args, **kwargs):
        raise Exception(
            "Use the 'get_instance' method to create an instance of this class."
        )

    def __init__(self):
        self._record = _BinaryTree()

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        cls._instance = None

    async def save(self, entity: PaymentEntity) -> None:
        self._record.save(entity)