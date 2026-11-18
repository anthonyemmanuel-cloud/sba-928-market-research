# Requirement 1: The sourced dataset and the facts behind the prompts

## Dataset summary

| Item | Value |
|---|---|
| Source | UCI Machine Learning Repository, Online Retail (dataset 352) |
| Period covered | December 01, 2010 to December 09, 2011 |
| Rows in the file | 541,909 |
| Product sales rows after cleaning | 524,621 |
| Cancelled rows removed | 9,288 |
| Orders reversed by a cancellation, removed | 3,188 |
| Countries | 38 |
| Different products | 3,986 |
| Identified customers | 4,322 |

## Facts per market research area

| Area | Facts | Prompts (6 per fact) |
|---|---|---|
| Market trends | 20 | 120 |
| Consumer behavior | 16 | 96 |
| Regional markets | 16 | 96 |
| Competitive positioning | 17 | 102 |

## Every fact with its correct insight

| ID | Area | Market | Question | Correct insight |
|---|---|---|---|---|
| M01 | Market trends | Global | Which month had the highest sales revenue? | Sales revenue peaked in November 2011. |
| M02 | Market trends | Global | Which full month had the lowest sales revenue? | The lowest full month for sales revenue was February 2011. |
| M03 | Market trends | Global | Which day of the week brings in the most revenue? | Thursday brings in the most revenue of any weekday. |
| M04 | Market trends | Global | On which day of the week are no sales recorded? | No sales are recorded on Saturday. |
| M05 | Market trends | Global | At what hour of the day are the most orders placed? | The busiest hour for orders starts at 12:00. |
| M06 | Market trends | Global | Which quarter had the highest sales revenue? | The strongest quarter for revenue was quarter 4 of 2011. |
| M07 | Market trends | Global | What was the total sales revenue for the whole period? | Total sales revenue for the period was about 9.9 million pounds. |
| M08 | Market trends | Global | What was the best-selling product by units in December 2010? | The best-selling product in December 2010 was World War 2 Gliders Asstd Designs. |
| M09 | Market trends | Global | What was the best-selling product by units in January 2011? | The best-selling product in January 2011 was White Hanging Heart T-Light Holder. |
| M10 | Market trends | Global | What was the best-selling product by units in February 2011? | The best-selling product in February 2011 was Empire Design Rosette. |
| M11 | Market trends | Global | What was the best-selling product by units in March 2011? | The best-selling product in March 2011 was Jumbo Bag Red Retrospot. |
| M12 | Market trends | Global | What was the best-selling product by units in April 2011? | The best-selling product in April 2011 was World War 2 Gliders Asstd Designs. |
| M13 | Market trends | Global | What was the best-selling product by units in May 2011? | The best-selling product in May 2011 was Small Popcorn Holder. |
| M14 | Market trends | Global | What was the best-selling product by units in June 2011? | The best-selling product in June 2011 was Jumbo Bag Red Retrospot. |
| M15 | Market trends | Global | What was the best-selling product by units in July 2011? | The best-selling product in July 2011 was Girls Alphabet Iron On Patches. |
| M16 | Market trends | Global | What was the best-selling product by units in August 2011? | The best-selling product in August 2011 was Assorted Colour Bird Ornament. |
| M17 | Market trends | Global | What was the best-selling product by units in September 2011? | The best-selling product in September 2011 was Jumbo Bag Red Retrospot. |
| M18 | Market trends | Global | What was the best-selling product by units in October 2011? | The best-selling product in October 2011 was World War 2 Gliders Asstd Designs. |
| M19 | Market trends | Global | What was the best-selling product by units in November 2011? | The best-selling product in November 2011 was Rabbit Night Light. |
| M20 | Market trends | Global | What was the best-selling product by units in December 2011? | The best-selling product in December 2011 was Popcorn Holder. |
| M21 | Consumer behavior | Global | What is the average order value? | The average order value is about 503 pounds. |
| M22 | Consumer behavior | Global | What is the median order value? | The median order value is about 302 pounds. |
| M23 | Consumer behavior | Global | How many items does an average order contain? | An average order contains about 272 items. |
| M24 | Consumer behavior | Global | What share of all invoices are cancellations? | About 15 percent of all invoices are cancellations. |
| M25 | Consumer behavior | Global | What share of identified customers ordered more than once? | About 65 percent of identified customers ordered more than once. |
| M26 | Consumer behavior | Global | How many orders does an identified customer place on average? | An identified customer places about 4.2 orders on average. |
| M27 | Consumer behavior | Global | What share of customer revenue comes from the top 10 percent of customers? | The top 10 percent of customers generate about 60 percent of identified customer revenue. |
| M28 | Consumer behavior | Global | What share of sales lines have no customer ID? | About 25 percent of sales lines have no customer ID. |
| M29 | Consumer behavior | UK | What is the average order value for customers in United Kingdom? | The average order value in United Kingdom is about 471 pounds. |
| M30 | Consumer behavior | Non-UK | What is the average order value for customers in Netherlands? | The average order value in Netherlands is about 3,048 pounds. |
| M31 | Consumer behavior | Non-UK | What is the average order value for customers in EIRE? | The average order value in EIRE is about 939 pounds. |
| M32 | Consumer behavior | Non-UK | What is the average order value for customers in Germany? | The average order value in Germany is about 462 pounds. |
| M33 | Consumer behavior | Non-UK | What is the average order value for customers in France? | The average order value in France is about 481 pounds. |
| M34 | Consumer behavior | Non-UK | What is the average order value for customers in Australia? | The average order value in Australia is about 2,587 pounds. |
| M35 | Consumer behavior | Non-UK | What is the average order value for customers in Switzerland? | The average order value in Switzerland is about 1,099 pounds. |
| M36 | Consumer behavior | Non-UK | What is the average order value for customers in Spain? | The average order value in Spain is about 605 pounds. |
| M37 | Regional markets | UK | What share of total revenue comes from the United Kingdom? | The United Kingdom generates about 85 percent of total revenue. |
| M38 | Regional markets | Global | How many countries does the retailer sell to? | The retailer has sales in 38 countries. |
| M39 | Regional markets | Non-UK | Which country is the largest market by revenue outside the United Kingdom? | Outside the United Kingdom, the largest market by revenue is Netherlands. |
| M40 | Regional markets | Non-UK | Which country is the second largest market by revenue outside the United Kingdom? | Outside the United Kingdom, the second largest market by revenue is EIRE. |
| M41 | Regional markets | Non-UK | Which country is the third largest market by revenue outside the United Kingdom? | Outside the United Kingdom, the third largest market by revenue is Germany. |
| M42 | Regional markets | Non-UK | Which country is the fourth largest market by revenue outside the United Kingdom? | Outside the United Kingdom, the fourth largest market by revenue is France. |
| M43 | Regional markets | Non-UK | Which country is the fifth largest market by revenue outside the United Kingdom? | Outside the United Kingdom, the fifth largest market by revenue is Australia. |
| M44 | Regional markets | UK | What is the best-selling product by units in United Kingdom? | The best-selling product in United Kingdom is World War 2 Gliders Asstd Designs. |
| M45 | Regional markets | Non-UK | What is the best-selling product by units in Netherlands? | The best-selling product in Netherlands is Rabbit Night Light. |
| M46 | Regional markets | Non-UK | What is the best-selling product by units in EIRE? | The best-selling product in EIRE is Pack Of 72 Retrospot Cake Cases. |
| M47 | Regional markets | Non-UK | What is the best-selling product by units in Germany? | The best-selling product in Germany is Round Snack Boxes Set Of4 Woodland. |
| M48 | Regional markets | Non-UK | What is the best-selling product by units in France? | The best-selling product in France is Rabbit Night Light. |
| M49 | Regional markets | Non-UK | What is the best-selling product by units in Australia? | The best-selling product in Australia is Mini Paint Set Vintage. |
| M50 | Regional markets | Non-UK | What is the best-selling product by units in Switzerland? | The best-selling product in Switzerland is Plasters In Tin Woodland Animals. |
| M51 | Regional markets | Non-UK | What is the best-selling product by units in Spain? | The best-selling product in Spain is Childrens Cutlery Polkadot Pink. |
| M52 | Regional markets | Non-UK | Among countries with at least 30 orders, which has the highest average order value? | Among countries with at least 30 orders, Netherlands has the highest average order value. |
| M53 | Competitive positioning | Global | Which product is the top earner by revenue? | The top product by revenue is Regency Cakestand 3 Tier. |
| M54 | Competitive positioning | Global | Which product is the second highest earner by revenue? | The second highest product by revenue is White Hanging Heart T-Light Holder. |
| M55 | Competitive positioning | Global | Which product is the third highest earner by revenue? | The third highest product by revenue is Party Bunting. |
| M56 | Competitive positioning | Global | Which product is the fourth highest earner by revenue? | The fourth highest product by revenue is Jumbo Bag Red Retrospot. |
| M57 | Competitive positioning | Global | Which product is the fifth highest earner by revenue? | The fifth highest product by revenue is Rabbit Night Light. |
| M58 | Competitive positioning | Global | Which product is the sixth highest earner by revenue? | The sixth highest product by revenue is Paper Chain Kit 50'S Christmas. |
| M59 | Competitive positioning | Global | Which product is the seventh highest earner by revenue? | The seventh highest product by revenue is Assorted Colour Bird Ornament. |
| M60 | Competitive positioning | Global | Which product is the eighth highest earner by revenue? | The eighth highest product by revenue is Chilli Lights. |
| M61 | Competitive positioning | Global | Which product is the ninth highest earner by revenue? | The ninth highest product by revenue is Spotty Bunting. |
| M62 | Competitive positioning | Global | Which product is the tenth highest earner by revenue? | The tenth highest product by revenue is Jumbo Bag Pink Polkadot. |
| M63 | Competitive positioning | Global | Which product has sold the most units overall? | The product with the most units sold overall is World War 2 Gliders Asstd Designs. |
| M64 | Competitive positioning | Global | What share of total revenue comes from the top 10 products? | The top 10 products generate about 8 percent of total revenue. |
| M65 | Competitive positioning | Global | Which earns more revenue, Regency Cakestand 3 Tier or White Hanging Heart T-Light Holder? | The bigger revenue earner of the two is Regency Cakestand 3 Tier. |
| M66 | Competitive positioning | Global | Which earns more revenue, Jumbo Bag Red Retrospot or Party Bunting? | The bigger revenue earner of the two is Party Bunting. |
| M67 | Competitive positioning | Global | Which earns more revenue, Paper Chain Kit 50'S Christmas or Rabbit Night Light? | The bigger revenue earner of the two is Rabbit Night Light. |
| M68 | Competitive positioning | Global | Which earns more revenue, Assorted Colour Bird Ornament or Chilli Lights? | The bigger revenue earner of the two is Assorted Colour Bird Ornament. |
| M69 | Competitive positioning | Global | Which earns more revenue, Spotty Bunting or Jumbo Bag Pink Polkadot? | The bigger revenue earner of the two is Spotty Bunting. |
