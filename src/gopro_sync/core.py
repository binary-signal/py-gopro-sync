from collections import namedtuple

GoProFile = namedtuple("GoProFile", "name modified size")

FileSizeMeta = namedtuple("FileSizeMeta", "value unit bytes_size")


def parse_size(size_str) -> FileSizeMeta:
    value, unit = float(size_str[:-1]), size_str[-1]

    GB = 1024 * 1024 * 1024
    MB = 1024 * 1024
    KB = 1024

    unit_mapping = {"G": GB, "M": MB, "k": KB}

    size_in_bytes = value * unit_mapping[unit]

    def __str__(self):
        return f"{self.value!r}{self.unit!r}"

    FileSizeMeta.__str__ = __str__

    return FileSizeMeta(value, unit, size_in_bytes)
