import json

from rest_framework import status
from rest_framework.response import Response


class ErrorResponse(Response):
    """
    API subclass from rest_framework response to simplify constructing error messages
    """
    def __init__(self, form=None, **kwargs):
        super(ErrorResponse, self).__init__(status=status.HTTP_400_BAD_REQUEST)

        data = kwargs
        if not data.get('detail'):
            data['detail'] = "Permintaan Anda tidak dapat diselesaikan"
            data["error_message"] = data['detail']

        # Build the error part of the message:
        # It should try to use "Code" part of the error as the key for the dict,
        # or Field name
        if form and form.errors.items():
            data['errors'] = {}

            for field, errors in json.loads(form.errors.as_json()).items():
                key = field

                # Since django 1.7 built in validation error also return code
                # Just replace the code from our stamps prefix
                code = errors[0].get('code')
                if code and code.startswith("stamps"):
                    key = errors[0]['code']

                message = errors[0]['message']
                data['errors'][key] = message
                data["detail"] = '%s: %s' % (key, message)
                data["error_code"] = errors[0].get('code') if errors[0].get('code') else "invalid_data"
                data["error_message"] = message if key == "__all__" else data["detail"]

                break
        self.data = data
