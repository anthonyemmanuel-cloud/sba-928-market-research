# Requirement 4: Original model compared with the fine-tuned model

## Overall

| Model | Correct | Accuracy | Relevance (word overlap, 0 to 1) |
|---|---|---|---|
| Original flan-t5-small | 0/69 | 0% | 0.01 |
| Fine-tuned | 49/69 | 71% | 0.73 |

## Accuracy by market research area

| Area | Original | Fine-tuned |
|---|---|---|
| Competitive positioning | 0/17 (0%) | 11/17 (65%) |
| Consumer behavior | 0/16 (0%) | 15/16 (94%) |
| Market trends | 0/20 (0%) | 15/20 (75%) |
| Regional markets | 0/16 (0%) | 8/16 (50%) |

## Accuracy by market (fairness check)

| Market | Original | Fine-tuned |
|---|---|---|
| Global | 0/46 (0%) | 33/46 (72%) |
| Non-UK | 0/20 (0%) | 15/20 (75%) |
| UK | 0/3 (0%) | 1/3 (33%) |

## Every test prompt, side by side

| Test prompt | Correct insight | Original model | Fine-tuned model | Fine-tuned correct? |
|---|---|---|---|---|
| What was the strongest month for revenue? | Sales revenue peaked in November 2011. | September | Sales peaked in November 2011. | Yes |
| What was the weakest full month for revenue? | The lowest full month for sales revenue was February 2011. | april | The weakest full month for revenue was February 2011. | Yes |
| What is the best weekday for sales? | Thursday brings in the most revenue of any weekday. | a weekday | Thursday brings in the most revenue of any weekday. | Yes |
| Is there a weekday when the retailer records no sales? | No sales are recorded on Saturday. | no | No sales are recorded on Saturday. | Yes |
| When during the day do customers order the most? | The busiest hour for orders starts at 12:00. | april | The busiest day for orders starts at 12:00. | Yes |
| What was the strongest quarter for revenue? | The strongest quarter for revenue was quarter 4 of 2011. | $1 billion | The strongest quarter for revenue was quarter 4 of 2011. | Yes |
| What do total sales add up to across the full dataset? | Total sales revenue for the period was about 9.9 million pounds. | a total of .2 | Total sales increase by about 272 pounds. | No |
| In December 2010, which item was the top seller by quantity? | The best-selling product in December 2010 was World War 2 Gliders Asstd Designs. | sand | The top product by quantity was Regency Cakestand 3 Tier. | No |
| In January 2011, which item was the top seller by quantity? | The best-selling product in January 2011 was White Hanging Heart T-Light Holder. | sand | The top product by quantity was White Hanging Heart T-Light Holder. | Yes |
| In February 2011, which item was the top seller by quantity? | The best-selling product in February 2011 was Empire Design Rosette. | sand | The top product by quantity was Empire Design Rosette. | Yes |
| In March 2011, which item was the top seller by quantity? | The best-selling product in March 2011 was Jumbo Bag Red Retrospot. | sand | The top product by quantity was Jumbo Bag Red Retrospot. | Yes |
| In April 2011, which item was the top seller by quantity? | The best-selling product in April 2011 was World War 2 Gliders Asstd Designs. | sand | The top product by quantity was World War 2 Gliders Asstd Designs. | Yes |
| In May 2011, which item was the top seller by quantity? | The best-selling product in May 2011 was Small Popcorn Holder. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In June 2011, which item was the top seller by quantity? | The best-selling product in June 2011 was Jumbo Bag Red Retrospot. | sand | The top product by quantity was Jumbo Bag Red Retrospot. | Yes |
| In July 2011, which item was the top seller by quantity? | The best-selling product in July 2011 was Girls Alphabet Iron On Patches. | sand | The top product by quantity was Girls Alphabet Iron On Patches. | Yes |
| In August 2011, which item was the top seller by quantity? | The best-selling product in August 2011 was Assorted Colour Bird Ornament. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In September 2011, which item was the top seller by quantity? | The best-selling product in September 2011 was Jumbo Bag Red Retrospot. | sand | The top product by quantity was Jumbo Bag Red Retrospot. | Yes |
| In October 2011, which item was the top seller by quantity? | The best-selling product in October 2011 was World War 2 Gliders Asstd Designs. | sand | The top product by quantity was World War 2 Gliders Asstd Designs. | Yes |
| In November 2011, which item was the top seller by quantity? | The best-selling product in November 2011 was Rabbit Night Light. | sand | The top product by quantity was Rabbit Night Light. | Yes |
| In December 2011, which item was the top seller by quantity? | The best-selling product in December 2011 was Popcorn Holder. | sand | The top product by quantity was Regency Cakestand 3 Tier. | No |
| What does a typical order come to on average? | The average order value is about 503 pounds. | a symbiotic relationship | The average order value is about 503 pounds. | Yes |
| How large is the median order? | The median order value is about 302 pounds. | 62 | The median order value is about 302 pounds. | Yes |
| How many units do customers buy in a typical order on average? | An average order contains about 272 items. | 1.2 | The average order value is about 503 pounds. | No |
| How common are cancelled orders as a share of invoices? | About 15 percent of all invoices are cancellations. | a share of invoices | About 15 percent of all invoices are cancellations. | Yes |
| How many identified customers came back for a second order, as a share? | About 65 percent of identified customers ordered more than once. | 59 | About 65 percent of identified customers ordered more than once. | Yes |
| On average, how often does an identified customer order? | An identified customer places about 4.2 orders on average. | annually | An identified customer places about 4.2 orders on average. | Yes |
| How concentrated is revenue among the biggest 10 percent of customers? | The top 10 percent of customers generate about 60 percent of identified customer revenue. | 5% | The biggest 10 percent of customers generate about 60 percent of identified customer revenue. | Yes |
| How much of the sales data is missing a customer ID? | About 25 percent of sales lines have no customer ID. | .5 | About 25 percent of sales lines have no customer ID. | Yes |
| In United Kingdom, what does a typical order average? | The average order value in United Kingdom is about 471 pounds. | a sulphur sulphur | The average order value in United Kingdom is about 471 pounds. | Yes |
| In Netherlands, what does a typical order average? | The average order value in Netherlands is about 3,048 pounds. | a slender slender | The average order value in Netherlands is about 3,048 pounds. | Yes |
| In EIRE, what does a typical order average? | The average order value in EIRE is about 939 pounds. | a styrofoam | The average order value in EIRE is about 939 pounds. | Yes |
| In Germany, what does a typical order average? | The average order value in Germany is about 462 pounds. | a sturgeon | The average order value in Germany is about 462 pounds. | Yes |
| In France, what does a typical order average? | The average order value in France is about 481 pounds. | a stag | The average order value in France is about 481 pounds. | Yes |
| In Australia, what does a typical order average? | The average order value in Australia is about 2,587 pounds. | a swath of a swath of a swath of a swath of a swath of a swath of | The average order value in Australia is about 2,587 pounds. | Yes |
| In Switzerland, what does a typical order average? | The average order value in Switzerland is about 1,099 pounds. | a swiss | The average order value in Switzerland is about 1,099 pounds. | Yes |
| In Spain, what does a typical order average? | The average order value in Spain is about 605 pounds. | a slender slender | The average order value in Spain is about 605 pounds. | Yes |
| How much of the retailer's revenue is from United Kingdom customers? | The United Kingdom generates about 85 percent of total revenue. | £8.9 million | The retailer has revenue of about 471 pounds. | No |
| What is the number of countries with recorded sales? | The retailer has sales in 38 countries. | 74 | Among countries with at least 27 sales, Netherlands has the highest recorded sales value. | No |
| Leaving out the United Kingdom, what is the largest country for revenue? | Outside the United Kingdom, the largest market by revenue is Netherlands. | england | The largest country by revenue is Netherlands. | Yes |
| Leaving out the United Kingdom, what is the second largest country for revenue? | Outside the United Kingdom, the second largest market by revenue is EIRE. | england | The second largest country by revenue is EIRE. | Yes |
| Leaving out the United Kingdom, what is the third largest country for revenue? | Outside the United Kingdom, the third largest market by revenue is Germany. | england | The third largest country by revenue is Germany. | Yes |
| Leaving out the United Kingdom, what is the fourth largest country for revenue? | Outside the United Kingdom, the fourth largest market by revenue is France. | england | The fourth largest country by revenue is France. | Yes |
| Leaving out the United Kingdom, what is the fifth largest country for revenue? | Outside the United Kingdom, the fifth largest market by revenue is Australia. | england | The fifth largest country by revenue is Australia. | Yes |
| In United Kingdom, which item is the top seller by quantity? | The best-selling product in United Kingdom is World War 2 Gliders Asstd Designs. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In Netherlands, which item is the top seller by quantity? | The best-selling product in Netherlands is Rabbit Night Light. | sand | The top product by quantity is Rabbit Night Light. | Yes |
| In EIRE, which item is the top seller by quantity? | The best-selling product in EIRE is Pack Of 72 Retrospot Cake Cases. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In Germany, which item is the top seller by quantity? | The best-selling product in Germany is Round Snack Boxes Set Of4 Woodland. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In France, which item is the top seller by quantity? | The best-selling product in France is Rabbit Night Light. | sand | The top product by quantity is Rabbit Night Light. | Yes |
| In Australia, which item is the top seller by quantity? | The best-selling product in Australia is Mini Paint Set Vintage. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In Switzerland, which item is the top seller by quantity? | The best-selling product in Switzerland is Plasters In Tin Woodland Animals. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| In Spain, which item is the top seller by quantity? | The best-selling product in Spain is Childrens Cutlery Polkadot Pink. | sand | The top product by quantity is Regency Cakestand 3 Tier. | No |
| Looking only at countries with 30 plus orders, where is the average order largest? | Among countries with at least 30 orders, Netherlands has the highest average order value. | switzerland | Among countries with at least 30 orders, Netherlands has the highest average order value. | Yes |
| What is the top revenue product in the range? | The top product by revenue is Regency Cakestand 3 Tier. | ad revenue | The top product by revenue is Regency Cakestand 3 Tier. | Yes |
| What is the second highest revenue product in the range? | The second highest product by revenue is White Hanging Heart T-Light Holder. | ad | The second highest product by revenue is White Hanging Heart T-Light Holder. | Yes |
| What is the third highest revenue product in the range? | The third highest product by revenue is Party Bunting. | ad | The third highest product in the range is Party Bunting. | Yes |
| What is the fourth highest revenue product in the range? | The fourth highest product by revenue is Jumbo Bag Red Retrospot. | ad | The fourth highest product in the range is Jumbo Bag Red Retrospot. | Yes |
| What is the fifth highest revenue product in the range? | The fifth highest product by revenue is Rabbit Night Light. | ad | The fifth highest product by revenue is Rabbit Night Light. | Yes |
| What is the sixth highest revenue product in the range? | The sixth highest product by revenue is Paper Chain Kit 50'S Christmas. | ad | The sixth highest product by revenue is Paper Chain Kit 50'S Christmas. | Yes |
| What is the seventh highest revenue product in the range? | The seventh highest product by revenue is Assorted Colour Bird Ornament. | ad | The seventh highest product by revenue is Assorted Colour Bird Ornament. | Yes |
| What is the eighth highest revenue product in the range? | The eighth highest product by revenue is Chilli Lights. | ad | The eighth highest product by revenue is Chilli Lights. | Yes |
| What is the ninth highest revenue product in the range? | The ninth highest product by revenue is Spotty Bunting. | ad | The ninth highest product by revenue is Spotty Bunting. | Yes |
| What is the tenth highest revenue product in the range? | The tenth highest product by revenue is Jumbo Bag Pink Polkadot. | ad | The tenth highest product by revenue is Jumbo Bag Pink Polkadot. | Yes |
| Across the whole period, which item leads on quantity sold? | The product with the most units sold overall is World War 2 Gliders Asstd Designs. | acetate | The whole period leads on quantity sold. | No |
| How concentrated is revenue in the ten leading products? | The top 10 products generate about 8 percent of total revenue. | 0.8 | The top 10 products generate about 8 percent of total revenue. | Yes |
| Comparing Regency Cakestand 3 Tier with White Hanging Heart T-Light Holder, which is the bigger revenue earner? | The bigger revenue earner of the two is Regency Cakestand 3 Tier. | rio s s s s s s s s s s s s s s s s s s s s s s | The bigger revenue earner of the two is White Hanging Heart T-Light Holder. | No |
| Comparing Party Bunting with Jumbo Bag Red Retrospot, which is the bigger revenue earner? | The bigger revenue earner of the two is Party Bunting. | jumbo bag red retrospot | The bigger revenue earner of the two is Jumbo Bag Red Retrospot. | No |
| Comparing Rabbit Night Light with Paper Chain Kit 50'S Christmas, which is the bigger revenue earner? | The bigger revenue earner of the two is Rabbit Night Light. | paper chain kit 50's christmas | The bigger revenue earner of the two is White Hanging Heart T-Light Holder. | No |
| Comparing Assorted Colour Bird Ornament with Chilli Lights, which is the bigger revenue earner? | The bigger revenue earner of the two is Assorted Colour Bird Ornament. | chilli lights | The bigger revenue earner of the two is Chilli Lights. | No |
| Comparing Spotty Bunting with Jumbo Bag Pink Polkadot, which is the bigger revenue earner? | The bigger revenue earner of the two is Spotty Bunting. | jumbo bag pink polkadot | The bigger revenue earner of the two is Jumbo Bag Pink Polkadot. | No |
