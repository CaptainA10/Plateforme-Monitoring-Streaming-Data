

  create or replace view `effidic-stage-2026`.`monitoring_datalake`.`stg_user_activity`
  OPTIONS()
  as with source as (
    select * from `effidic-stage-2026`.`monitoring_datalake`.`user_activity`
),

renamed as (
    select
        event_id,
        user_id,
        event_type,
        timestamp as event_timestamp,
        page_id,
        metadata
    from source
)

select * from renamed;

