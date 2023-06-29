# TTDS Project - Recipe Search Engine

### Supported Features

1. Free text search
Examples: I want salads with fruits like orange, strawberry and apple
I want recipes similar to apple pies.
Indian cuisine recipes.

2. Recommendations are not shown for all the recipes but sharing a few examples where
recommendations will be shown.
Examples: Festive Fruit Salad, Hawaiian Baked Beans And Franks, BarbaraS
Sugarless Apple Pie, French Bread Pizza.

3. Boolean Search supported with multiple operators “AND, OR and NOT”
You need to select “other” from the drop-down next to the search button.
Examples: Honey AND Chilli AND Potato, cheese AND sugar AND NOT milk, Banana
AND apples AND orange AND kiwi, cheese AND sugar AND milk.
4. Phrase Search
You need to select “other” from the drop-down next to the search button.
"hot milk" AND sugar, "hot milk" AND sugar AND NOT flour, “ground cinnamon"
5. TFIDF/BM25 can be selected for free search as retrieval models, by default TFIDF is the
default retrieval model.
6. Expand Query:
You need to tick-mark the “Expand Query” option under the search box.
7. Nutrition Calculator
Nutrition values for all the ingredients in the recipe are shown in the table.

### Known Issues:
1. A lot of recipes have the same title but the ingredients are different for those recipes.
2. Since out of a 2.2 million recipes dataset, we trained our clustering model only on 18,000 recipes so recommended recipes fields for most of the searched recipes will be empty.

