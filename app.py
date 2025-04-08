import argparse
from binascii import hexlify, unhexlify


def gpon_sn_converter(sn: str | bytes, encoding: str = 'utf-8', strict: bool = False) -> str:
    """
    Универсальный конвертер серийных номеров GPON:
    - ASCII -> HEX
    - HEX -> ASCII

    Примеры:
        'HWTC542D049B' -> '48575443542D049B'
        '48575443542D049B' -> 'HWTC542D049B'

    :param sn: Серийный номер (строка или байты)
    :param encoding: Кодировка для преобразования (по умолчанию 'utf-8')
    :param strict: Если True — выбрасывает ошибку при нераспознанном формате
    :return: Преобразованный серийный номер (строка)
    """
    if isinstance(sn, str):
        sn = sn.encode(encoding)

    sn = sn.replace(b'-', b'')

    try:
        if len(sn) == 12:
            prefix_ascii = sn[:4].decode(encoding)
            suffix = sn[4:].decode(encoding).upper()
            if prefix_ascii.isascii():
                return hexlify(sn[:4]).decode(encoding).upper() + suffix

        elif len(sn) == 16:
            prefix_ascii = unhexlify(sn[:8]).decode(encoding)
            suffix = sn[8:].decode(encoding).upper()
            return prefix_ascii + suffix

    except Exception as e:
        if strict:
            raise ValueError(f"Could not parse SN: {sn!r} — {e}")

    raise ValueError(f"Unknown or unsupported SN format: {sn!r}")


def main():
    parser = argparse.ArgumentParser(description="GPON Serial Number Converter (ASCII <-> HEX)")
    parser.add_argument("sn", type=str, help="Serial number in ASCII or HEX format")
    parser.add_argument("-e", "--encoding", default="utf-8", help="Encoding to use (default: utf-8)")
    parser.add_argument("-s", "--strict", action="store_true", help="Strict mode: fail on unknown format")

    args = parser.parse_args()

    try:
        result = gpon_sn_converter(args.sn, encoding=args.encoding, strict=args.strict)
        print(result)

    except Exception as ex:
        print(f"Error: {ex}")
        exit(1)


if __name__ == "__main__":
    main()
