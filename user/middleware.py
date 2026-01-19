# middleware.py
# from django.utils.deprecation import MiddlewareMixin
# from ipware import get_client_ip

# class VisitorInfoMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Get client IP
#         ip, is_routable = get_client_ip(request)
#         request.client_ip = ip
#         request.ip_is_routable = is_routable
#         return None 