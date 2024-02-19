# from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

# class mycustompag(PageNumberPagination):
#     page_size=3
#     # max_page_size=10
#     # page_query_param=10
    
# c

# this is for limit offset pagination 
# class mycustompag(LimitOffsetPagination):
#     max_limit=3
    
# this is pagination for pagenumberpagination 
# class mycustompag(CursorPagination):
#     page_size=3
#     ordering='-price' #this is compulsory for using it in the cursor pagination
    
    
from rest_framework.pagination import PageNumberPagination

class mycustompag(PageNumberPagination):
    page_size=6
    max_page_size=4