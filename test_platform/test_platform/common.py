from django.http import JsonResponse

def Response(code=None,message=None,data=[]):
    if code == None:
        code = 10200

    if message == None:
        message = 'success'

    return JsonResponse({
        "code":code,
        "message":message,
        "data":data
    })