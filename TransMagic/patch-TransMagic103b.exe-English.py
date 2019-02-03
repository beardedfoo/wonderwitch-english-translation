
#!/usr/bin/env python3
# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import sys

from io import BytesIO

DEFAULT_ENCODING_IN='shiftjis'
DEFAULT_ENCODING_OUT='utf-8'

def patch(s, location, original, replacement, encoding_in=DEFAULT_ENCODING_IN, encoding_out=DEFAULT_ENCODING_OUT, pad=None):
    # Encode the expected and replacement text as bytes
    original_bytes = original.encode(encoding_in)
    replacement_bytes = replacement.encode(encoding_out)

    # Add any specified padding as necessary
    if pad != None:
        if len(pad.encode(encoding_out)) != 1:
           raise ValueError('only single-byte padding is supported')
        while len(replacement_bytes) < len(original_bytes):
            replacement_bytes += pad.encode(encoding_out)

    # Check the existing value is correct at this location
    s.seek(location)
    existing = s.read(len(original_bytes))
    if existing != original_bytes:
        raise ValueError('unexpected value @ {:X} found "{}" instead'.format(location, existing))

    # Ensure the replacement fits
    if len(replacement_bytes) != len(original_bytes):
        raise ValueError('replacement value does not match original size @ {:X}'.format(location))

    # Write the patch
    s.seek(location)
    s.write(replacement_bytes)


def multipatch(s, locations, original, replacement, encoding_in=DEFAULT_ENCODING_IN, encoding_out=DEFAULT_ENCODING_OUT, pad=None):
    for l in locations:
        patch(s, l, original, replacement, encoding_in=encoding_in, encoding_out=encoding_out, pad=pad)


def main():
    # Read in the original exe
    with open('C:\\WWitch\\beta\\TransMagic103b.exe', 'rb') as f:
        exe = BytesIO(f.read())

    # /rom0/ (プログラムエリア)
    patch(exe, 0xdd030, "/rom0/ (プログラムエリア)", "/rom0/ (program)", pad='\0')

    # /ram0/ (ワークエリア)
    patch(exe, 0xdd04b, "/ram0/ (ワークエリア)", "/ram0/ (work)", pad='\0')

    # カートリッジ
    multipatch(exe, [0xdefce, 0xdcd1b], "カートリッジ", "Cartridge", pad='\0')

    # WonderWitchに接続されていません
    multipatch(
        exe,
        [0xb89de, 0xb89fe, 0xb8a1e, 0xb8a3e, 0xb8bc4, 0xb8c97,
         0xb8d64, 0xb8efa, 0xb8f29, 0xb8f49, 0xb902d, 0xb9151,
         0xb924d, 0xb9456, 0xb9c15, 0xb9cf8, 0xb9d3f],
         "WonderWitchに接続されていません",
         "WonderWitch connection error", pad='\0')

    # プロトコルログ
    patch(exe, 0xdea5a, "プロトコルログ", "Protocol Log", pad='\0')

    # バイト
    # Using a space pad here as these could occur mid-string
    multipatch(exe, [0xb9e1e, 0xb9e2d, 0xb9e39, 0xb9e48, 0xb9e4f], "バイト", " bytes", pad=' ')

    # マイコンピュータ
    patch(exe, 0xdd0a6, "マイコンピュータ", "My Computer", pad='\0')

    # 名前
    multipatch(exe, [0xdd10e, 0xdcd80, 0xe0ecf], "名前", "Name")

    # 接続中
    # This should be "connection" etc., but that's too big
    multipatch(exe, [0xb8d89, 0xd9499], "接続中", "Link", pad='\0')

    # ファイル(&F)
    patch(exe, 0xdec8d, "ファイル(&F)", "&File", pad='\0')

    # カートリッジ(&C)
    patch(exe, 0xdeea1, "カートリッジ(&C)", "&Cartridge", pad='\0')

    # ヘルプ(&H)
    patch(exe, 0xdf0ee, "ヘルプ(&H)", "&Help", pad='\0')

    # 接続(&C)
    patch(exe, 0xdecb6, "接続(&C)", "&Connect", pad='\0')

    # 切断(&D)
    # Should be "Disconnect", but that's too big
    patch(exe, 0xdecf5, "切断(&D)", "Close", pad='\0')

    # プロトコルログ保存(&S)
    patch(exe, 0xded4e, "プロトコルログ保存(&S)", "&Save Log", pad='\0')

    # シリアルポート設定...
    patch(exe, 0xdee04, "シリアルポート設定...", "Serial Settings", pad='\0')

    # プロトコルログクリア
    patch(exe, 0xded9c, "プロトコルログクリア", "Clear Log", pad='\0')

    # エリア整頓(&F)
    patch(exe, 0xdeecd, "エリア整頓(&F)", "Defragment", pad='\0')

    # エリア整頓
    patch(exe, 0xe04a7, "エリア整頓", "Defragment")

    # 終了(&X)
    patch(exe, 0xdee68, "終了(&X)", "E&xit", pad='\0')

    # エリア全クリア(&A)
    patch(exe, 0xdef27, "エリア全クリア(&A)", "Format", pad='\0')

    # エリア全クリア
    patch(exe, 0xe04df, "エリア全クリア", "Format", pad='\0')

    # 時刻設定...
    patch(exe, 0xdef82, "時刻設定...", "Time/Date", pad='\0')

    # アップグレード...
    patch(exe, 0xdf069, "アップグレード...", "Upgrade", pad='\0')

    # バックアップ...
    patch(exe, 0xdf0ad, "バックアップ...", "Backup", pad='\0')

    # TransMagicについて...
    patch(exe, 0xdf11d, "TransMagicについて...", "About TransMagic", pad='\0')

    # アイコンの整列
    multipatch(exe, [0xdfe3b, 0xe02ff], "アイコンの整列", "Arrange Icons", pad='\0')

    # 名前順
    multipatch(exe, [0xdfe6e, 0xe0333], "名前順", "ByName", pad='\0')

    # サイズ順
    multipatch(exe, [0xdfeb8, 0xe037f], "サイズ順", "BySize", pad='\0')

    # 日付順
    multipatch(exe, [0xdff04, 0xe03cd], "日付順", "ByDate", pad='\0')

    # 最新の情報に更新
    multipatch(exe, [0xdff6e, 0xe0440], "最新の情報に更新", "Refresh", pad='\0')

    # フォルダ作成...
    patch(exe, 0xdffdf, "フォルダ作成...", "New Folder", pad='\0')

    # 開く(&O)
    patch(exe, 0xe0056, "開く(&O)", "&Open", pad='\0')

    # WonderWitchへ送信
    patch(exe, 0xe00b8, "WonderWitchへ送信", "Send To WWitch", pad='\0')

    # 削除(&D)
    patch(exe, 0xe0127, "削除(&D)", "&Delete", pad='\0')

    # 名前の変更(&M)
    patch(exe, 0xe016b, "名前の変更(&M)", "Rena&me", pad='\0')

    # 空き容量 
    patch(exe, 0xb89b3, "空き容量", "Free:  ", pad='\0')

    # 名称未設定.txt
    patch(exe, 0xb8f1a, "名称未設定.txt", "wwitch-log.txt", pad='\0')

    # テキストファイル
    # This occurs mid-string, so we must not null terminate. Pad with space.
    patch(exe, 0xe020f, "テキストファイル", "Text Document", pad=' ')
    
    # リッチテキストファイル
    # This occurs mid-string, so we must not null terminate. Pad with space.
    patch(exe, 0xe022d, "リッチテキストファイル", "Rich Text Document", pad=' ')

    # WonderWitchをモニタモードで立ち上げて
    # Recv System しておいてください。
    #
    # OSをアップグレードします。よろしいですか？
    patch(exe, 0xb9a6c, "WonderWitchをモニタモードで立ち上げて", "Launch WonderWitch in monitor mode.\r\n", pad=' ')
    patch(exe, 0xb9a93, "Recv System しておいてください。\r\n", "Do not poweroff WonderWitch!\r\n", pad=' ')
    patch(exe, 0xb9ab7, "OSをアップグレードします。よろしいですか？", "Proceed with OS upgrade?", pad=' ')

    # 切断中
    # TODO: Improve the following translation. translate.google.com says this means "cutting", but that doesn't make sense.
    patch(exe, 0xdec34, "切断中", "Cut?", pad='\0')

    # 接続
    # This should be connection, but that doesn't fit.
    patch(exe, 0xdebb1, "接続", "Link")

    # 通信ポート：
    patch(exe, 0xd921e, "通信ポート：", "Port:", pad='\0')

    # 通信速度
    patch(exe, 0xd9262, "通信速度", "Speed:", pad='\0')

    # キャンセル
    multipatch(exe, [0xd9414, 0xd95f9, 0xd9af2, 0xe0a8b, 0xe0cbf, 0xe1175, 0xe178c], "キャンセル", "Cancel", pad='\0')

    # フォルダを選択してください
    patch(exe, 0xb8995, "フォルダを選択してください", "Select Folder:", pad='\0')

    # 通信設定
    patch(exe, 0xd90e7, "通信設定", "Serial", pad='\0')

    # %sを全クリアします。エリア内のファイルは全て消去されます。
    # よろしいですか？
    patch(exe, 0xb9104, "%sを全クリアします。エリア内のファイルは全て消去されます。", "All files on %s will be deleted.", pad=' ')
    patch(exe, 0xb9140, "よろしいですか？", "Proceed?", pad='\0')

    # WonderWitchに接続しています・・・
    patch(exe, 0xd9599, "WonderWitchに接続しています・・・", "Connecting to WonderWitch...", pad='\0')

    # フォルダ作成
    patch(exe, 0xd968e, "フォルダ作成", "New Folder", pad='\0')

    # 作成
    patch(exe, 0xd982b, "作成", "Make", pad='\0')

    # キャンセル
    patch(exe, 0xd9891, "キャンセル", "Cancel", pad='\0')

    # 時刻設定
    patch(exe, 0xd995f, "時刻設定", "Set Time", pad='\0')

    # カートリッジ時刻
    patch(exe, 0xd9b54, "カートリッジ時刻", "Cartridge Time", pad='\0')

    # 設定時刻
    patch(exe, 0xd9c5e, "設定時刻", "Set Time", pad='\0')

    # 作成するフォルダの名前の入力してください。
    patch(exe, 0xd97c6, "作成するフォルダの名前の入力してください。", "Please enter folder name", pad='\0')

    # サイズ
    multipatch(exe, [0xdcdb2, 0xdd140], "サイズ", "Size", pad='\0')

    # 日付
    multipatch(exe, [0xdcdcc, 0xdd15a], "日付", "Date", pad='\0')

    # 属性
    patch(exe, 0xdcde4, "属性", "Attr", pad='\0')

    # 説明
    multipatch(exe, [0xdcdf4, 0xe0f0d], "説明", "Info", pad='\0')

    # 通信ポートのオープンに失敗しました。
    multipatch(exe, [0xb9651, 0xb8d90], "通信ポートのオープンに失敗しました。", "Failed to open comm port", pad='\0')

    # TODO: This doesn't work
    # Set the dialog font/charset to a western one instead of Japanese
    # patch(exe, 0xdd177, "SHIFTJIS_CHARSET", "ANSI_CHARSET", pad='\0')
    # patch(exe, 0xdd1ba, "ＭＳ Ｐゴシック", "MS PGothic", pad='\0')

    # WonderWitchをモニタモードで立ち上げて
    # Send System しておいてください。
    #
    # OSをバックアップします。よろしいですか？
    patch(exe, 0xb9885, "WonderWitchをモニタモードで立ち上げて\r\n", "Launch WonderWitch in monitor mode.\r\n", pad=' ')
    patch(exe, 0xb98ac, "Send System しておいてください。\r\n", "Do not poweroff WonderWitch!\r\n", pad=' ')
    patch(exe, 0xb98d0, "OSをバックアップします。よろしいですか？", "Proceed with OS backup?", pad='\0')

    # パケット数：
    patch(exe, 0xe0a40, "パケット数：", "Packets: ", pad='\0')

    # ファイル転送中・・・
    patch(exe, 0xe0b1a, "ファイル転送中・・・", "Transferring file", pad='\0')

    # 転送中
    patch(exe, 0xe0c48, "転送中", "Xfer..", pad='\0')

    # TODO: This causes a crash on program launch
    # 以下の情報で送信します
    # patch(exe, 0xe0d9d, "以下の情報で送信します", "Send the following:", pad=' ')

    # FreyaOSを転送しています
    patch(exe, 0xe08d2, "FreyaOSを転送しています", "FreyaOS Upgrade/Backup", pad=' ')

    # Write a new exe
    with open('C:\\WWitch\\beta\\TransMagic103b-EnglishPatched.exe', 'wb') as f:
        exe.seek(0)
        f.write(exe.read())

    return 0


if __name__ == '__main__':
    main()
