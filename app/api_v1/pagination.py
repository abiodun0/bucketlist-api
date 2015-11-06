from flask import url_for, current_app
from ..models import Bucketlist, Item


def paginate(objectset, endpoint, options,_class,id=None):

	print options

	q = options.get('q', "", type=str)
	page = options.get('page', 1, type=int)
	limit_given = options.get('limit',1,type=int)
	limit = limit_given if limit_given else current_app.config['DEFAULT_PER_PAGE']
	pagination = objectset.order_by('date_modified desc').filter(_class.name.contains(q)).paginate(page, per_page=limit,error_out=False)
	items = pagination.items
	prev_page = url_for(endpoint,id=id,page=page - 1, _external=True) if pagination.has_prev else None

	next_page = url_for(endpoint,id=id,page=page + 1, _external=True) if pagination.has_next else None


	json =  {
		"items": [item.to_json() for item in items],
		"prev_page": prev_page,
		"next_page": next_page,
		"total_item": pagination.total,
		"current_page": page
		}
	return json