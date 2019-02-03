#!/usr/bin/env python3
# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import os
import sys

from io import BytesIO

DEFAULT_ENCODING_IN='shiftjis'
DEFAULT_ENCODING_OUT='utf-8'

def patch(s, location, original, replacement, encoding_in=DEFAULT_ENCODING_IN, encoding_out=DEFAULT_ENCODING_OUT):
    # Encode the expected and replacement text as bytes
    original_bytes = original.encode(encoding_in)
    replacement_bytes = replacement.encode(encoding_out)

    # Check the existing value is correct at this location
    s.seek(location)
    existing = s.read(len(original_bytes))
    if existing != original_bytes:
        raise ValueError('unexpected value @ {:X}'.format(location))

    # Ensure the replacement fits
    if len(replacement_bytes) > len(original_bytes):
        raise ValueError('replacement value too large @ {:X}'.format(location))

    # Write the patch
    s.seek(location)
    s.write(replacement_bytes)


def multipatch(s, locations, original, replacement, encoding_in=DEFAULT_ENCODING_IN, encoding_out=DEFAULT_ENCODING_OUT):
    for l in locations:
        patch(s, l, original, replacement, encoding_in=encoding_in, encoding_out=encoding_out)


def main():
    # Read in the original exe
    with open('TransMagic103b.exe', 'rb') as f:
        exe = BytesIO(f.read())

    # /rom0/ (プログラムエリア)
    patch(exe, 0xdd030, "/rom0/ (プログラムエリア)", "/rom0/ (program)\0")

    # /ram0/ (ワークエリア)
    patch(exe, 0xdd04b, "/ram0/ (ワークエリア)", "/ram0/ (work)\0")

    # カートリッジ
    multipatch(exe, [0xdefce, 0xdcd1b], "カートリッジ", "Cartridge\0")

    # WonderWitchに接続されていません
    multipatch(
        exe,
        [0xb89de, 0xb89fe, 0xb8a1e, 0xb8a3e, 0xb8bc4, 0xb8c97,
         0xb8d64, 0xb8efa, 0xb8f29, 0xb8f49, 0xb902d, 0xb9151,
         0xb924d, 0xb9456, 0xb9c15, 0xb9cf8, 0xb9d3f],
         "WonderWitchに接続されていません",
         "WonderWitch connection error\0")

    # プロトコルログ
    patch(exe, 0xdea5a, "プロトコルログ", "Protocol Log\0")

    # バイト
    multipatch(exe, [0xb9e1e, 0xb9e2d, 0xb9e39, 0xb9e48, 0xb9e4f], "バイト", "bytes\0")

    # マイコンピュータ
    patch(exe, 0xdd0a6, "マイコンピュータ", "My Computer\0")

    # 名前
    multipatch(exe, [0xdd10e, 0xdcd80], "名前", "Name")

    # 接続中
    # This should be "connection" etc., but it's too big
    multipatch(exe, [0xb8d89, 0xd9499], "接続中", "Link\0")

    # ファイル(&F)
    patch(exe, 0xdec8d, "ファイル(&F)", "Download(&F)")

    # Write a new exe
    with open('TransMagic103b-EnglishPatched.exe', 'wb') as f:
        exe.seek(0)
        f.write(exe.read())

    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main())
