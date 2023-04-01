import binascii
from django.shortcuts import render
import rsa


# Create your views here.
user_message = ""
def second(request):
    global user_message
    if request.method == "POST":
        key_pub, key_priv = keys()
        if "crypto" in request.POST:
            user_message = request.POST["crypto_text"]
            answer = {
                "ans": crypto(user_message, key_pub),
                "start": key_pub
            }
        elif "decrypto" in request.POST:
            answer = {
                "ans": decrypto(user_message, key_priv),
                "start": key_priv
            }
    else:
        answer = {}
    return render(request, "second.html", answer)


def keys():
    (_keyPublic, _keyPrivate) = rsa.newkeys(512)
    return _keyPublic, _keyPrivate


def crypto(message, key_public):
    msg = message.encode("utf-8")
    crpt = rsa.encrypt(msg, key_public)
    return crpt


def decrypto(message, key_private):
    msg = message.encode("utf-8")
    dcrpt = rsa.decrypt(msg, key_private)
    return dcrpt
