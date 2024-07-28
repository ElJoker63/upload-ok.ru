# OK.ru Video Uploader

Este script permite subir automáticamente videos a tu perfil de OK.ru utilizando Python.

## Requisitos

- Python 3.6 o superior
- Biblioteca `requests` (puedes instalarla con `pip install requests`)

## Configuración

1. Clona este repositorio o descarga el script `main.py`.

2. Instala las dependencias:

```console
pip install requests
```

3. Obtén las cookies de tu sesión de OK.ru:
- Inicia sesión en OK.ru desde tu navegador.
- Usa una extensión para exportar cookies (como "EditThisCookie" para Chrome o "Cookie Quick Manager" para Firefox).
- Exporta las cookies en formato Netscape y guárdalas en un archivo llamado `cookie.txt` en el mismo directorio que el script.

## Uso

1. Coloca los videos que deseas subir en un directorio.

2. Modifica el script `main.py`:
- Cambia la variable `video_directory` a la ruta de tu directorio de videos:
  ```python
  video_directory = 'path/to/your/video/directory'
  ```

3. Ejecuta el script:

```console
python main.py
```

4. El script subirá cada video en el directorio especificado a tu perfil de OK.ru.

## Notas importantes

- Asegúrate de que tus cookies sean válidas y no hayan expirado. Si experimentas problemas de autenticación, actualiza el archivo `cookie.txt` con nuevas cookies.
- Este script está diseñado para uso personal y no comercial. Asegúrate de cumplir con los términos de servicio de OK.ru.
- El script soporta archivos de video con extensiones .mp4, .avi, .mov, .flv y .mkv. Si necesitas soporte para otros formatos, modifica la lista de extensiones en el código.

## Solución de problemas

Si encuentras algún problema:

1. Verifica que las cookies en `cookie.txt` sean válidas y actuales.
2. Asegúrate de que tienes una conexión a internet estable.
3. Comprueba que tienes los permisos necesarios para subir videos en tu cuenta de OK.ru.
4. Si el problema persiste, revisa el archivo `upload_page.html` generado por el script para obtener más información sobre posibles errores.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una mejora, no dudes en abrir un issue o enviar un pull request.

## Descargo de responsabilidad

Este script se proporciona "tal cual", sin garantía de ningún tipo. Úsalo bajo tu propia responsabilidad y asegúrate de cumplir con los términos de servicio de OK.ru.