# Example Usage

```
cd src && chmod +x interface.py
./interface.py
```
No CLI arguments are needed, script will prompt for them when necessary.

First prompt will be for an All Recipes URL. Enter it without quotes. Then enter the desired transform when prompted.

# Presentations

In your zip file submission, all groups must include a short video (maximum of 10 minutes) named "demo_video" demonstrating your solution.

# Demo Video Requirements

- Transform https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/ (Links to an external site.) to VEGETARIAN;
- Transform https://www.allrecipes.com/recipe/244716/shirataki-meatless-meat-pad-thai/ (Links to an external site.) to NON-VEGETARIAN;
- Transform https://www.allrecipes.com/recipe/16167/beef-bourguignon-i/ (Links to an external site.) to HEALTHY;
- Transform https://www.allrecipes.com/recipe/228285/teriyaki-salmon/ (Links to an external site.) to UNHEALTHY;
- Use at least two of the following on the optional transformations:
A. https://www.allrecipes.com/recipe/229293/korean-saewoo-bokkeumbap-shrimp-fried-rice/ (Links to an external site.)
B. https://www.allrecipes.com/recipe/7757/tiramisu-cheesecake/ (Links to an external site.)
C. https://www.allrecipes.com/recipe/73303/mexican-rice-iii/ (Links to an external site.)
- One final recipe at your group's discretion that best demonstrates your solution.

# Project Deliverables

- All code must be in Python 3. You can use any Python package or Python NLP toolkit, other than python-allrecipes, which you may not use.
- You must use a publicly accessible repository such as Github, and commit code regularly. When pair programming, note in the commit message those who were present and involved. We use these logs to verify complaints about AWOL teammates, and to avoid penalizing the entire group for one student’s violation of academic integrity. We don’t look at the commits unless there’s something really wrong with the code, or there’s a complaint.
- Please use the Python standard for imports described here: https://www.python.org/dev/peps/pep-0008/#imports (Links to an external site.)
- If you use a DB, it must be Mongo DB, and you must provide the code you used to populate your database.
- Your code must be runnable by the TAs. Thus, your repository must include a readme.txt file that lists the version of the programming language you used, and all dependencies. Any modules that are not part of the standard install of your programming language should be included in this list, along with information on the code repository from which it can be downloaded (e.g. for python, pip or easy_install). If you used code that you instead put in a file in your project’s working directory, then a copy of that file should be provided along with the code you wrote; the readme and/or comments in such files should clearly state that the code was not written by your team.

# The Project

For your second project, you’ll be creating a recipe transformer. Your recipe transformer must complete the following tasks:

1. Accept the URL of a recipe from AllRecipes.com, and programmatically fetch the page.
2. Parse it into the recipe data representation your group designs. Your parser should be able to recognize:
  - Ingredients
  	- Ingredient name
  	- Quantity
  	- Measurement (cup, teaspoon, pinch, etc.)
  	- (optional) Descriptor (e.g. fresh, extra-virgin)
  	- (optional) Preparation (e.g. finely chopped)
  	- Tools – pans, graters, whisks, etc.
  - Methods
  	- Primary cooking method (e.g. sauté, broil, boil, poach, etc.)
	- (optional) Other cooking methods used (e.g. chop, grate, stir, shake, mince, crush, squeeze, etc.)
  - Steps – parse the directions into a series of steps that each consist of ingredients, tools, methods, and times
3. Ask the user what kind of transformation they want to do.
- To and from vegetarian (REQUIRED)
- To and from healthy (REQUIRED)
- Style of cuisine (AT LEAST ONE REQUIRED)
- Additional Style of cuisine (OPTIONAL)
- Double the amount or cut it by half (OPTIONAL)
- Cooking method (from bake to stir fry, for example) (OPTIONAL)
- Gluten- or lactose-free (OPTIONAL)

If you come up with your own transformation idea, feel free to ask if it would be an acceptable substitute. We encourage innovation.

4. Transform the recipe along the requested dimension, using your system’s internal representation for ingredients, cooking methods, etc.
5. Display the transformed recipe in a human-friendly format.

Your transformations should work on any given recipe. Make sure to test using a wide variety of recipes. Some recipes will be harder than others to transform, and we will use a range of recipe complexity when grading.
