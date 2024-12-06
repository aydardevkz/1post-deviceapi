class AppDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'app_service':
            return 'app_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'app_service':
            return db == 'app_db'
        return None


class ExpressDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'express_service':
            return 'express_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'express_service':
            return db == 'express_db'
        return None


class NotificationDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'notification_service':
            return 'notification_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'notification_service':
            return db == 'notification_db'
        return None


class UserDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'user_service':
            return 'user_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'user_service':
            return db == 'user_db'
        return None


class DefaultDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'default_service':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'default_service':
            return db == 'default'
        return None


class AuthDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth_service':
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth_service':
            return db == 'auth_db'
        return None


class TradeDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'trade_service':
            return 'trade_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'trade_service':
            return db == 'trade_db'
        return None


class IdentityDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'identity_service':
            return 'identity_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'identity_service':
            return db == 'identity_db'
        return None


class OpenDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'open_service':
            return 'open_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'open_service':
            return db == 'open_db'
        return None
