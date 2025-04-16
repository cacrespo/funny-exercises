import humanize

import dlt

from dlt.sources.sql_database import sql_database


def load_select_tables_from_database() -> None:
    """Use the sql_database source to reflect an entire database schema and
    load select tables from it."""
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name="selected_tables",
        destination="postgres",
        dataset_name="workshop_dataset",
    )

    source_1 = sql_database().with_resources("ventas")

    # Add incremental config to the resources. "updated" is a timestamp column
    # in these tables that gets used as a cursor
    source_1.ventas.apply_hints(incremental=dlt.sources.incremental("updated_at"))
    source_1.ventas.apply_hints(primary_key="id")

    # Run the pipeline. The merge write disposition merges existing rows in the
    # destination by primary key
    info = pipeline.run(source_1, write_disposition="merge")
    print(info)

    # Load some other tables with replace write disposition. This overwrites
    # the existing tables in destination
    source_2 = sql_database().with_resources("cursos", "clientes")
    info = pipeline.run(source_2, write_disposition="replace")
    print(info)

    # Load a table incrementally with append write disposition
    # this is good when a table only has new rows inserted, but not updated
    source_3 = sql_database().with_resources("participantes")

    info = pipeline.run(source_3, write_disposition="append")
    print(info)


def load_entire_database() -> None:
    """Use the sql_database source to completely load all tables in a
    database"""
    pipeline = dlt.pipeline(
        pipeline_name="entire_db",
        destination="postgres",
        dataset_name="workshop_dataset",
    )

    source = sql_database()

    # Run the pipeline. For a large db this may take a while
    info = pipeline.run(source, write_disposition="replace")
    print(
        humanize.precisedelta(
            pipeline.last_trace.finished_at - pipeline.last_trace.started_at
        )
    )
    print(info)


if __name__ == "__main__":
    load_select_tables_from_database()
    load_entire_database()
