try:
    with open('equipos.json', 'r', encoding='utf-8') as infile:
        data = infile.read()
    with open('equipos_utf8.json', 'w', encoding='utf-8') as outfile:
        outfile.write(data)
    print("Archivo guardado como equipos_utf8.json")
    print(data[:200])
except UnicodeDecodeError as e:
    print(f"Error de codificación: {e}")