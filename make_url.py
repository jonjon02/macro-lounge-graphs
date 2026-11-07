import subprocess
import lzstring
code = open("goods_market.py").read()
url = ("https://molab.marimo.io/new/wasm/?embed=true&mode=read&show-code=false&show-chrome=false#code/"
       + lzstring.LZString().compressToEncodedURIComponent(code))

def writeClipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

writeClipboard(url)