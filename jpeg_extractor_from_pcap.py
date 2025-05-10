import re

with open("footage.pcap", "rb") as f:
    data = f.read()

matches = re.findall(b'\xff\xd8.*?\xff\xd9', data, re.DOTALL)

for i, jpeg in enumerate(matches):
    with open(f'frame_{i:04d}.jpg', 'wb') as out:
        out.write(jpeg)