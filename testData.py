import os
import sys
import logging
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from PIL import Image
import uuid
from array import array
from pymongo import MongoClient
from statistics import mode
from views.db import mongo

if os.path.exists("views/env.py"):
    from views.env import *


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = "random_string"
mongo.init_app(app)


print("Sarting program")


def wipeDataBase():
    mongo.db.recipe_project.drop()
    mongo.db.fs.chunks.drop()
    mongo.db.fs.files.drop()


def insertRecipe(recipeName, ingredients, how_to, vegetarian, pathImage, author):
    try:
        extention = os.path.splitext(pathImage)
        if extention:
            randomFileName = str(uuid.uuid1()) + str(extention[1])
        else:
            randomFileName = str(uuid.uuid1()) + ".jpg"
        # recipeImage = open(pathImage,'rb')
        with open(pathImage, "rb") as recipeImage:
            imageId = mongo.save_file(randomFileName, recipeImage)

        # r = fs.get(recipeImage).read()
        print(imageId)
        mongo.db.recipe_project.insert_one(
            {"recipeName": recipeName,
             "ingredients": ingredients,
             "how_to": how_to,
             "vegetarian": vegetarian,
             "recipe_image_Id": randomFileName,
             "author": author.lower()})
    except Exception as exception:
        exception_message = str(exception)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print(exception_message)


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
wipeDataBase()
insertRecipe("Apple Tart", [
    "225 g Plain White Flour or 2 Cups",
    "130 g Irish Butter Unsalted (room temp) or a 1/2 Cup",
    "1 tsp Salt",
    "2 tbsp Caster Sugar",
    "45 ml Cold Water or Milk or 3 tbsp", "4 Large Cooking apples approx 675 g / 1 1/2 lbs",
    "75 g Caster Sugar or 6 tbsp",
    "A little bit of milk to glaze or egg yold mixed with milk"],
    ["Preheat oven to 200°C/400°F/Gas 6.",
     "Place butter/margarine in freezer for about 15 minutes to harden.",
     "Sieve flour into a bowl",
     "Grate hard butter/margarine into the flour. You may need a little flour on your fingers for this.",
     "Using a knife, mix grated butter/margarine into flour.",
     "Add sufficient water and mix to a soft dough with the knife.",
     "Turn onto a floured board and knead lightly.",
     "Roll out half the pastry to the size of an oven proof plate.",
     "Arrange apples on the pastry.",
     "Sprinkle with sugar to sweeten.",
     "Roll remaining pastry to cover the apples.",
     "Dampen edge of base pastry with cold water to seal.",
     "Press top pastry over apples to make the tart. Seal the edges by using the back of a knife to form a crust. Then cut at 1'/3cm intervals to form a scalloped edge, if liked!",
     "Put a cut on top of pastry to allow steam to escape and bake for 25-35 minutes approx."],
    False, "./testData/appletart.jpg", "billy joel")
insertRecipe("Pancake", ["100g plain flour", "Pinch of salt", "1 Bord Bia Quality Assured egg", "300 ml milk", "1 tablsp. melted butter or sunflower oil"],
             ["Sift the flour and salt into a mixing bowl and make a well in the centre.",
              "Crack the egg into the well; add the melted butter or oil and half the milk. Gradually draw the flour into the liquid by stirring all the time with a wooden spoon until all the flour has been incorporated and then beat well to make a smooth batter.",
              "Stir in the remaining milk. Alternatively, beat all the ingredients together for 1 minute in a blender or food processor.", "Leave to stand for about 30 minutes, then stir again before using.",
              "To make the pancakes, heat a small heavy-based frying until very hot and then turn the heat down to medium.",
              "Lightly grease with oil and then ladle in enough batter to coat the base of the pan thinly (about 2 tablsp.), tilting the pan so the mixture spreads evenly.",
              "Cook over a moderate heat for 1-2 minutes or until the batter looks dry on the top and begins to brown at the edges. Flip the pancake over with a palette knife or fish slice and cook the second side.",
              "Turn onto a plate, smear with a little butter, sprinkle of sugar and a squeeze of lemon juice and serve."],
             False,
             "./testData/pancake.jpg", "user 1")

insertRecipe("Scones", ["350g self-raising flour, plus more for dusting", "¼ tsp salt", "1 tsp baking powder",
                        "85g butter and cut into cubes", "3 tbsp caster sugar", "175ml milk", "1 tsp vanilla extract", "squeeze lemon juice", "beaten egg to glaze",
                        "jam and clotted cream, to serve"],
             ["Heat oven to 220C/fan 200C/gas 7.",
              "Tip 350g self-raising flour into a large bowl with ¼ tsp salt and 1 tsp baking powder, then mix.",
              "Add 85g butter cubes, then rub in with your fingers until the mix looks like fine crumbs then stir in 3 tbsp caster sugar.",
              "Put 175ml milk into a jug and heat in the microwave for about 30 secs until warm, but not hot.",
              "Add 1 tsp vanilla extract and a squeeze of lemon juice, then set aside for a moment.",
              "Put a baking sheet in the oven.",
              "Make a well in the dry mix, then add the liquid and combine it quickly with a cutlery knife – it will seem pretty wet at first.",
              "Scatter some flour onto the work surface and tip the dough out. Dredge the dough and your hands with a little more flour, then fold the dough over 2-3 times until it’s a little smoother. Pat into a round about 4cm deep.",
              "Take a 5cm cutter (smooth-edged cutters tend to cut more cleanly, giving a better rise) and dip it into some flour. Plunge into the dough, then repeat until you have four scones. You may need to press what’s left of the dough back into a round to cut out another four.",
              "Brush the tops with a beaten egg, then carefully place onto the hot baking tray.",
              "Bake for 10 mins until risen and golden on the top. Eat just warm or cold on the day of baking, generously topped with jam and clotted cream. ",
              "If freezing, freeze once cool. Defrost, then put in a low oven (about 160C/fan140C/gas 3) for a few mins to refresh."],
             False,
             "./testData/scones.jpg", "billy joel")
insertRecipe("Chorizo & mozzarella gnocchi bake", ["1 tbsp olive oil", "1 onion finely, chopped", "2 garlic cloves, crushed",
                                                   "120g chorizo, diced", "2 x 400g cans chopped tomatoes",
                                                   "1 tsp caster sugar", "600g fresh gnocchi",
                                                   "125g mozzarella ball, cut into chunks",
                                                   "small bunch of basil, torn",
                                                   "green salad, to serve"],
             ["Heat the oil in a medium pan over a medium heat. Fry the onion and garlic for 8-10 mins until soft. Add the chorizo and fry for 5 mins more. Tip in the tomatoes and sugar, and season. Bring to a simmer, then add the gnocchi and cook for 8 mins, stirring often, until soft. Heat the grill to high.",
              "Stir ¾ of the mozzarella and most of the basil through the gnocchi. Divide the mixture between six ovenproof ramekins, or put in one baking dish. Top with the remaining mozzarella, then grill for 3 mins, or until the cheese is melted and golden. Season, scatter over the remaining basil and serve with green salad."],
             False,
             "./testData/chorizoPasta.jpg", "cian orourke")


insertRecipe("Creamy herb chicken", ["4 chicken breasts (pounded 1/2-inch thin)", "2 teaspoons each of onion powder and garlic powder", "1 teaspoon fresh chopped parsley", "1/2 teaspoon each of dried thyme and dried rosemary*", "salt and pepper , to season", "4 cloves garlic , minced (or 1 tablespoon minced garlic)", "1 teaspoon fresh chopped parsley", "1/2 teaspoon each of dried thyme and dried rosemary", "1 cup milk (or half and half)*", "Salt and freshly ground black pepper , to taste", "1 teaspoon cornstarch mixed with 1 tablespoon water , until smooth"],
             ["Coat chicken breasts with the onion and garlic powders and herbs. Season generously with salt and pepper.",
              "Heat 1 tablespoon of oil a large pan or skillet over medium-high heat and cook chicken breasts until opaque and no longer pink inside (about 5 minutes each side, depending on thickness). Transfer to a plate; set aside.", "To the same pan or skillet, heat another 2 teaspoons of olive oil and sauté garlic, with parsley, thyme and rosemary, for about 1 minute, or until fragrant.", "Stir in milk (or cream); season with salt and pepper, to taste.", "Bring to a boil; add the cornstarch mixture to the centre of the pan, quickly stirring, until sauce has thickened slightly. Reduce heat and simmer gently for a further minute to allow the sauce to thicken more.", "Return chicken to the skillet. Sprinkle with extra herbs if desired. Serve immediately."],
             False,
             "./testData/creamy-herb-chicken.jpg", "user 1")
insertRecipe("Caponata pasta", ["4 tbsp olive oil(or use the oil from your chargrilled veg, see below)",
                                "1 large onion",
                                "4 garlic cloves, finely sliced",
                                "250g chargrilled Mediterranean veg (peppers and aubergines, if possible) from a jar, pot or deli counter, drained if in oil (you can use this oil in place of the olive oil) and roughly chopped",
                                "400g can chopped tomatoes", "1 tbsp small capers", "2 tbsp raisins", "350g rigatoni, penne or another short pasta shape", "bunch of basil, leaves picked", " parmesan(or vegetarian alternative), shaved, to serve"],
             ["Tip in the mixed veg, tomatoes, capers and raisins. Season well and simmer, uncovered, for 10 mins, or until you have a rich sauce.",
              "Meanwhile, boil the kettle. Pour the kettleful of water into a large pan with a little salt and bring back to the boil. Add the pasta and cook until tender with a little bite, then drain, reserving some of the pasta water. Tip the pasta into the sauce, adding a splash of pasta water if it needs loosening. Scatter with the basil leaves and parmesan, if you like, and serve straight from the pan"],
             True,
             "./testData/caponata-pasta.jpg", "user 1")

insertRecipe("Sweetcorn & courgette fritters",
             ["198g can sweetcorn, drained",
              "2 spring onions",
              "50g courgette, grated",
              "1 tsp smoked paprika",
              "50g self raising flour", "5 eggs, 1 beaten, 4 for poaching", "40ml milk", "4 tbsp sweet chilli sauce", "juice 1 lime", "1 tbsp vegetable oil", "mixed leave, to serve"],
             ["Mix the sweetcorn, spring onions, courgette, paprika, flour, beaten egg, milk and some seasoning in a large bowl and set aside.",
              "Put a large pan of water on to boil. In a bowl, mix the chilli sauce with the lime juice and set aside.",
              "Heat the oil in a large, non-stick pan and spoon in four burger-sized mounds of the fritter mixture, spaced apart (you may need to do this in two batches). When brown on the underside, turn over and cook for 3 mins more until golden.",
              "Meanwhile, poach the eggs in the simmering water for 2-3 mins until cooked and the yolks are runny. Remove with a slotted spoon. Serve the fritters topped with a poached egg, mixed leaves and a drizzle of the chilli dressing."],
             True,
             "./testData/sweetcorn-courgette-fritters.jpg", "user 1")
