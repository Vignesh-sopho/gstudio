''' -- imports from python libraries -- '''
# import os -- Keep such imports here
import json

''' -- imports from installed packages -- '''
from django.shortcuts import render_to_response  # , render
from django.template import RequestContext
from django.http import Http404

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId


''' -- imports from application folders/files -- '''
from gnowsys_ndf.ndf.models import node_collection, triple_collection, gridfs_collection, NodeJSONEncoder

def query_doc(request, doc_id_or_name=None):

	if ObjectId.is_valid(doc_id_or_name):
		doc_id_or_name = ObjectId(doc_id_or_name)

	query_res = node_collection.find({
								'$or': [
										{'_id': doc_id_or_name},
										{'name': unicode(doc_id_or_name)}
									]
								})

	result = []
	for each_doc in query_res:
		result.append(json.dumps(each_doc, cls=NodeJSONEncoder, sort_keys=True))

	return render_to_response('ndf/dev_query_doc.html',
					        {'result': result},
					        context_instance=RequestContext(request)
						    )


def render_test_template(request):
	test_node = node_collection.one({"name":"home",'_type':"Group"})
	return render_to_response(
        'ndf/test_template.html',
        {"node":test_node},
        context_instance=RequestContext(request)
    )
	
