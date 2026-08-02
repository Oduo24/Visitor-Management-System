from app.extensions import db


class DatabaseSession:
    """
    Centralized database transaction manager.
    """

    @staticmethod
    def commit():
        """Commit the current transaction."""
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def rollback():
        """Rollback the current transaction."""
        db.session.rollback()

    @staticmethod
    def flush():
        """
        Flush pending changes to the database without committing.
        Useful when you need generated IDs before the transaction is committed.
        """
        db.session.flush()