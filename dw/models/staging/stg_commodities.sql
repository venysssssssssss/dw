with source as (
    select
        "Date",
        "Close",
        simbolo
    from {{source ('dbsalesaovivo_e0w1', 'commodities')}}
),

renamed as (

    select
        cast("Date" as date) as data,
        "Close" as valor_fechamento,
        simbolo as simbolo
    from 
        source
)


select * from renamed