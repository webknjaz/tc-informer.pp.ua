import logging

logger = logging.getLogger(__name__)

from StudentsSocialNotifier.model import User, Post, PeriodicDeliveryTask, Delivery
import cherrypy

from sqlalchemy import desc

def find_user_by_id(session, id):
    id = int(id)
    return session.query(User).get(id)

def find_user_by_vk(session, vk):
    return session.query(User)\
        .filter(User.vk_id == vk).first()

def delete_user_by_id(session, id):
    id = int(id)
    return session.query(User)\
        .filter(User.id == id).delete()

def delete_post_by_id(session, id):
    id = int(id)
    return session.query(Post)\
        .filter(Post.id == id).delete()

def add_user(session, name, surname, bydad, vk_id):
    """adding user to db"""
    kwargs = {
            'name': name,
            'surname': surname,
            'bydad': bydad
            }
    if vk_id:
        kwargs.update({'vk_id': vk_id})
    if get_users_list(session)['count'] < 1:
        kwargs.update({'is_admin': True})
    
    u = User(**kwargs)
    session.add(u)
    session.commit()
    return u

def add_post(session, **kwargs):
    """adding user to db"""
    assert kwargs.get('msg') is not None

    kwargs = {
            'content': kwargs['msg'],
            'author_id': cherrypy.session.get('user')['id'],
    }
    
    p = Post(**kwargs)
    session.add(p)
    session.commit()
    
    users = session.query(User.id).filter(User.id != p.author_id).all()
    for (u,) in users:
        try:
            d = Delivery(post_id = p.id, user_id = u)
            session.add(d)
            session.commit()
        except:
            pass
        try:
            t = PeriodicDeliveryTask(when = None, todo = {'action':'notify_via_vk','deliver_to':u})
            session.add(t)
            session.commit()
        except:
            pass
    return p

def get_users_list(session, start = 0, ulimit = 20):
    return {
            'count':session.query(User).count(), 
            'list': session.query(User)\
                .filter(User.id>start).limit(ulimit)
            }

def add_first_user(session, name, surname, bydad):
    """adding user to db"""
    assert get_users_list(session)['count'] < 1, 'There should be a clean db'
    kwargs = {
            'name': name,
            'surname': surname,
            'bydad': bydad,
            'vk_id': cherrypy.session['user']['VK']['viewer_id'],
            'is_admin': True
            }
    
    u = User(**kwargs)
    session.add(u)
    session.commit()
    return u

def get_posts_list(session, start = 0, ulimit = 5):
    return session.query(Post).order_by(desc(Post.created)).offset(start).limit(ulimit)
