from rembg import remove


def rmv_bgrnd(input_path, output_path):
    """Функция обработки фотографии - удаление фона"""
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)
