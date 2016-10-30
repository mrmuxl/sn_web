import json
from django.http import HttpResponse
def json_return(json_data,ensure_ascii=True):
	return HttpResponse(json.dumps(json_data,ensure_ascii),content_type="application/json")