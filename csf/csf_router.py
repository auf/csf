class CSFRouter(object):
    """
    A router to control all database operations on models in the
    formulaire application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'formulaire' or model._meta.app_label == 'references':
            return 'formulaire_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'formulaire' or model._meta.app_label == 'references':
            return False
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'formulaire':
           return True
        return None

    def allow_syncdb(self, db, model):
        if model._meta.app_label == 'formulaire' or model._meta.app_label == 'references':
            return False
        return None

