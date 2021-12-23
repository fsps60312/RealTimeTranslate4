def is_chinese(c: str):
    assert(len(c) == 1)
    return '\u4e00' <= c and c <= '\u9fff'