import sqlalchemy as sa
from paginate_sqlalchemy import SqlalchemyOrmPage #<- provides pagination
from ..meta import DBSession
from ..blog_record import BlogRecord

class BlogRecordService(object):

    @classmethod
    def all(cls):
        return DBSession.query(BlogRecord).order_by(sa.desc(BlogRecord.created))

    @classmethod
    def by_id(cls, id):
        return DBSession.query(BlogRecord).filter(BlogRecord.id == id).first()

    @classmethod
    def get_paginator(cls, request, page=1):
        query = DBSession.query(BlogRecord).order_by(sa.desc(BlogRecord.created))
        query_params = request.GET.mixed()

        def url_maker(link_page):
            # replace page param with values generated by paginator
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return SqlalchemyOrmPage(query, page, items_per_page=5,
                                 url_maker=url_maker)
