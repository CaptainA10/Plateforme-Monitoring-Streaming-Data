with staging as (
    select * from {{ ref('stg_user_activity') }}
),

daily_metrics as (
    select
        date(event_timestamp) as activity_date,
        event_type,
        count(*) as event_count,
        count(distinct user_id) as unique_users
    from staging
    group by 1, 2
)

select * from daily_metrics
order by activity_date desc, event_count desc
