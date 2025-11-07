import pathlib


def generate_unique_name(path: pathlib.Path, original_name: str) -> str:
    """
    Генерирует униклаьное имя для файлов или дирикторий
    """
    base_name = original_name
    counter = 1

    while (path / base_name).exists():
        name_parts = original_name.split('.')
        if len(name_parts) > 1:
            base_name = f"{'.'.join(name_parts[:-1])}_{counter}.{name_parts[-1]}"
        else:
            base_name = f"{original_name}_{counter}"
        counter += 1

    return base_name
