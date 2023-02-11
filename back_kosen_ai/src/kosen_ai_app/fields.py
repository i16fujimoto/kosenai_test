from django.db import models


class ListField(models.CharField):
    """リストを保存するためのフィールド

    Note:
        "0.6, 1, 5.81, 4.9"のようにカンマ区切りの文字列をリストとして扱える
        要素の型はすべて同じである必要がある

    Args:
        val_type (Any): 要素の型. ex: int, float, str

    """

    description = "list of elements in desired type"

    def __init__(self, val_type, *args, **kwargs):
        self.val_type = val_type
        super(ListField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["val_type"] = self.val_type
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return list(map(self.val_type, value.split(",")))

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return None
        return list(map(self.val_type, value.split(",")))

    def get_prep_value(self, value):
        if value is None:
            return None
        return ",".join(map(str, value))
