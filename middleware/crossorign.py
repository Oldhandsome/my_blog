from django.utils.deprecation import MiddlewareMixin


class CrossOrigin(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        response['Access-Control-Allow-Methods'] = "GET,POST"
        if request.method == "OPTIONS":
            # the way of methods of complex request
            response['Access-Control-Allow-Methods'] = "PUT,DELETE,GET,POST"
            # the way of header of complex request
            response['Access-Control-Allow-Headers'] = "Content-Type"
        return response
