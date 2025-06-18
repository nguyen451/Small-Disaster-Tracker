SELECT "type", "count"
FROM (
    SELECT "type", COUNT("type") AS "count"
    FROM "disasters"
    GROUP BY "type"
) WHERE (
    "count" = (
        SELECT MIN("count") FROM (
            SELECT COUNT("type") AS "count" FROM "disasters"
            GROUP BY "type"
        )
    )
)