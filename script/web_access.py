import urllib
import urllib.request
import ssl

def get_data(url):
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    req = urllib.request.Request(url=url)
    try:
        with urllib.request.urlopen(req, context=context) as f:
            result = f.read().decode()
            # print("data is ...")
            # print(result)
        return result
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')
        return None
