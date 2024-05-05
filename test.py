import magic

# pip install python-magic-bin==0.4.14
try:
    mime_type= magic.from_buffer(open(r"C:\Users\soos\Downloads\1.mkv", "rb").read(2048), mime=True).split("/")[0]
except FileNotFoundError:
    raise





print(mime_type)