"""schema init

Revision ID: 2201a3f6d9a0
Revises:
Create Date: 2018-09-14 17:40:00.173286

"""
from pathlib import Path
import os
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2201a3f6d9a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    sql_file_path = Path(os.path.dirname(os.path.realpath(__file__))) / 'sql' / 'schema_init.sql'
    with open(sql_file_path, 'r') as sql_file:
        data = sql_file.read()
    op.execute(data)


def downgrade():
    # from https://stackoverflow.com/questions/536350/drop-all-the-tables-stored-procedures-triggers-constraints-and-all-the-depend
    op.execute('''
        /* Drop all non-system stored procs */
        DECLARE @name VARCHAR(128)
        DECLARE @SQL VARCHAR(254)

        SELECT @name = (SELECT TOP 1 [name] FROM sysobjects WHERE [type] = 'P' AND category = 0 ORDER BY [name])

        WHILE @name is not null
        BEGIN
            SELECT @SQL = 'DROP PROCEDURE [dbo].[' + RTRIM(@name) +']'
            EXEC (@SQL)
            PRINT 'Dropped Procedure: ' + @name
            SELECT @name = (SELECT TOP 1 [name] FROM sysobjects WHERE [type] = 'P' AND category = 0 AND [name] > @name ORDER BY [name])
        END
        GO

        /* Drop all views */
        DECLARE @name VARCHAR(128)
        DECLARE @SQL VARCHAR(254)

        SELECT @name = (SELECT TOP 1 [name] FROM sysobjects WHERE [type] = 'V' AND category = 0 ORDER BY [name])

        WHILE @name IS NOT NULL
        BEGIN
            SELECT @SQL = 'DROP VIEW [dbo].[' + RTRIM(@name) +']'
            EXEC (@SQL)
            PRINT 'Dropped View: ' + @name
            SELECT @name = (SELECT TOP 1 [name] FROM sysobjects WHERE [type] = 'V' AND category = 0 AND [name] > @name ORDER BY [name])
        END
        GO

        /* Drop all functions */
        DECLARE @name VARCHAR(128)
        DECLARE @SQL VARCHAR(254)

        SELECT @name = (SELECT TOP 1 [name] FROM sysobjects WHERE [type] IN (N'FN', N'IF', N'TF', N'FS', N'FT') AND category = 0 ORDER BY [name])

        WHILE @name IS NOT NULL
        BEGIN
    ''')
