with source as (
    select * from {{ source('raw_data', 'user_activity') }}
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

select * from renamed
