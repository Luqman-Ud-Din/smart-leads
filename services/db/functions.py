from django.db.models import Func


class ConvertTimeZone(Func):
    template = "%(expressions)s AT TIME ZONE '%(from_tz)s' AT TIME ZONE '%(to_tz)s'"

    def __init__(self, expression, from_tz, to_tz, **extra):
        super().__init__(expression, from_tz=from_tz, to_tz=to_tz, **extra)

    def as_postgresql(self, compiler, connection):
        return super().as_sql(
            compiler, connection,
            template="%(expressions)s AT TIME ZONE '%(from_tz)s' AT TIME ZONE '%(to_tz)s'"
        )

    def as_mysql(self, compiler, connection):
        return super().as_sql(
            compiler, connection,
            template="CONVERT_TZ(%(expressions)s, '%(from_tz)s', '%(to_tz)s')"
        )

    def as_sqlite(self, compiler, connection):
        # For SQLite, just return the original expression, assuming Python handles the conversion
        return super().as_sql(
            compiler, connection,
            template="%(expressions)s"
        )
