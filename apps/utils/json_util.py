import json
from django.http import HttpResponse
def json_return(json_data):
	return HttpResponse(json.dumps(json_data),content_type="application/json")