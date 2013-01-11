from ..import mgmt_view
from ...util import find_catalog

class SearchViews(object):
    def __init__(self, request):
        self.request = request

    @mgmt_view(
        name='search',
        permission='sdi.sdi.manage-contents',
        tab_condition=False,
        renderer='json'
    )
    def search(self):
        request = self.request
        context = request.context
        query = request.params['query']
        query = query + '*'

        catalog = find_catalog(context, 'system')
        allowed = catalog['allowed']
        name = catalog['name']
        text = catalog['text']

        q = (allowed.allows(request, 'sdi.view') & text.eq(query))
        resultset = q.execute()
        resultset = resultset.sort(name, limit=10)

        results = []
        for res_id in resultset.ids:
            res = resultset.resolver(res_id)
            url = request.sdiapi.mgmt_path(res, '@@manage_main')
            result = dict(label=res.title, url=url)
            results.append(result)

        return results
