# Scraping EWG

We provide scraping of products, and ingredients.

## Product scraping

`python ewg.py CATEGORY PAGE PER_PAGE`

## Ingredient scraping

Scrapes ingredients based on existing `product` results, so ensure that you've completed `product` scraping first.

`python ingredients.py "HAZARD LEVEL" LIMIT ORDER`

### Misc

`product_id` column in `ingredients` table is an array table of ints. Each match of ingredient will result in automatic merging of product_id array.

To de-dupe results in this array, use a SQL query like:
`SELECT (select array_agg(distinct val) from ( select unnest(:product_id) as val ) as u ) FROM :ingredients;`
with update
`UPDATE ingredients i SET product_id = (SELECT (select array_agg(distinct val) from ( select unnest(product_id) as val ) as u ) FROM ingredients ii WHERE ii.id = i.id)`
