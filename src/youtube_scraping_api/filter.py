import json
from .utils import getInitialData, searchDict
from .urls import BASE_URL

class SearchFilter:
	"""Filter for search results
	
	:param type:
		(optional) Type of search result
	:type type: str or None
	:param features:
		(optional) Features of vidoes
	:type features: list or None
	:param sort_by:
		(optional) Criteria of sorting search results
	:type sort_by: str or None
	:param upload_date:
		(optional) Upload date of videos
	:type upload_date: datetime or None

	:rtype: Object[SearchFilter]
	"""
	def __init__(self, type=None, features=None, sort_by=None, upload_date=None):
		self.type = (type, 'Type')
		self.features = (features, 'Features')
		self.sort_by = (sort_by, 'Sort by')
		self.upload_date = (upload_date, 'Upload date')

def getFilteredUrl(session, base_url, filter):
	"""Generate valid search url that includes query string filter

	:param session: Requests session
	:type session: Session
	:param base_url: Base search url that includes only query string
	:type base_url: str
	:param filter: Search filter that defined by user
	:type filter: SearchFilter
	:return: Valid search url
	:rtype: str
	"""
	url = base_url
	for i in [filter.type, filter.sort_by, filter.upload_date]:
		if i[0]:
			raw = getInitialData(session.get(url).text)
			filter_groups = [i['searchFilterGroupRenderer'] for i in next(searchDict(raw, "searchSubMenuRenderer"))['groups']]
			target_group = [f for f in filter_groups if f['title']['simpleText']==i[1]][0]
			if not target_group: raise AttributeError(f'Filter type {i} not found')
			filters = [i['searchFilterRenderer'] for i in target_group['filters']]
			target_filter = [f for f in filters if f['label']['simpleText']==i[0]]
			if not target_filter: raise AttributeError('Filter "{}" not found in {}'.format(i[0], target_group['title']['simpleText']))
			try: url = BASE_URL+next(searchDict(target_filter, 'url'))
			except: pass

	if filter.features[0] and isinstance(filter.features[0], list):
		for i in filter.features[0]:
			if i and isinstance(i, str):
				raw = getInitialData(session.get(url).text)
				filter_groups = [i['searchFilterGroupRenderer'] for i in next(searchDict(raw, "searchSubMenuRenderer"))['groups']]
				target_group = [f for f in filter_groups if f['title']['simpleText']=='Features'][0]
				if not target_group: raise AttributeError(f'Filter type {i} not found')
				filters = [i['searchFilterRenderer'] for i in target_group['filters']]
				target_filter = [f for f in filters if f['label']['simpleText']==i]
				if not target_filter: raise AttributeError('Filter "{}" not found in {}'.format(i[0], target_group['title']['simpleText']))
				try: url = BASE_URL+next(searchDict(target_filter, 'url'))
				except: pass
			else:
				raise TypeError('Features filter elements must be a string')
	return url