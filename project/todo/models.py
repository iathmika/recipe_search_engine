from pymongo import MongoClient

class RecipeData:
    _instance = None
    _client = MongoClient("mongodb://localhost:27017/")
    _db = _client["TTDS"]
    _collection = _db["recipe"]

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = RecipeData()
        return cls._instance

    def get_all_recipes(self):
        return list(self._collection.find({}))

    def get_recipe_by_id(self, recipe_id):
        return self._collection.find_one({"id": recipe_id})
    def get_recipe_by_title(self, recipe_title):
        return self._collection.find_one({"title": recipe_title})

    def get_recipe_fields(self, recipe_id):
        recipe = self._collection.find_one({"id": recipe_id})
        title = recipe.get("title")
        ingredients = recipe.get("ingredients")
        directions = recipe.get("directions")
        link = recipe.get("link")
        source = recipe.get("source")
        NER = recipe.get("NER")
        return (title, ingredients, directions, link, source, NER)

    def update_recipe(self, recipe_id, title=None, ingredients=None, directions=None, link=None, source=None, NER=None):
        recipe = self._collection.find_one({"id": recipe_id})
        if not recipe:
            return None

        updates = {}
        if title:
            updates["title"] = title
        if ingredients:
            updates["ingredients"] = ingredients
        if directions:
            updates["directions"] = directions
        if link:
            updates["link"] = link
        if source:
            updates["source"] = source
        if NER:
            updates["NER"] = NER

        self._collection.update_one({"id": recipe_id}, {"$set": updates})
        return self._collection.find_one({"id": recipe_id})

    def update_recipe_title(self, recipe_id, title):
        return self.update_recipe(recipe_id, title=title)

    def update_recipe_ingredients(self, recipe_id, ingredients):
        return self.update_recipe(recipe_id, ingredients=ingredients)

    def update_recipe_directions(self, recipe_id, directions):
        return self.update_recipe(recipe_id, directions=directions)

    def update_recipe_link(self, recipe_id, link):
        return self.update_recipe(recipe_id, link=link)

    def update_recipe_source(self, recipe_id, source):
        return self.update_recipe(recipe_id, source=source)

    def update_recipe_NER(self, recipe_id, NER):
        return self.update_recipe(recipe_id, NER=NER)

    def delete_recipe(self, recipe_id):
        result = self._collection.delete_one({"id": recipe_id})
        return result.deleted_count

    def search_recipes(self, query):
        query_result = self._collection.find({
            "$text": {
                "$search": query
            }
        })
        return query_result
     

if __name__ == "__main__":
   

      recipe_data = RecipeData.getInstance()
      recipes = recipe_data.get_recipe_by_title("No-Bake Nut Cookies")
      recipes_2 = recipe_data.get_recipe_by_id("10")
      print(recipes)
      print("recipes_2: ",recipes_2)
        #recipes = recipe_data.search_recipes(2)
        #query_result = list(recipes)
        #for result in query_result:
#    print(result)
