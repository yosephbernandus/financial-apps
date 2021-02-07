def get_client_ip(request):
    """ Modified from http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django """
    cf_original_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_original_ip:
        return cf_original_ip

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # Get the last IP in http_x_forwarded_for http://en.wikipedia.org/wiki/X-Forwarded-For#Format
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
