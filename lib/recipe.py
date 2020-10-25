class Recipe(object):

    def __init__(self):
        self.key = ""                   #   0
        self.number = ""                #   1
        self.craft_type = ""            #   2
        self.recipe_level_table = ""    #   3
        self.item_result = ""           #   4
        self.amount_result = ""         #   5
        self.is_secondary = ""
        self.material_quality_factor = ""
        self.difficulty_factor = ""
        self.quality_factor = ""
        self.durability_factor = ""
        self.required_craftsmanship = ""
        self.required_control = ""
        self.quick_synth_craftsmanship = ""
        self.quick_synth_control = ""
        self.secret_recipe_book = ""
        self.can_quick_synth = ""
        self.can_hq = ""
        self.exp_rewarded = ""
        self.status_required = ""
        self.item_required = ""
        self.is_specialization_required = ""
        self.is_expert = ""
        self.patch_number = ""

        self.num_ingredients = 0
        self.ingredients = []

    def __repr__(self):
        return F"{self.key} \
\n\t Number: {self.number} \
\n\t Craft Type: {self.craft_type} \
\n\t Recipe Level Table: {self.recipe_level_table} \
\n\t Item Result: {self.item_result} \
\n\t Amount Result: {self.amount_result} \
\n\t Is Secondary: {self.is_secondary} \
\n\t Material Quality Factor: {self.material_quality_factor} \
\n\t Difficulty Factor: {self.difficulty_factor} \
\n\t Quality Factor: {self.quality_factor} \
\n\t Durability Factor: {self.durability_factor} \
\n\t Required Craftsmanship: {self.required_craftsmanship} \
\n\t Required Control: {self.required_control} \
\n\t Quick Synth Craftsmanship: {self.quick_synth_craftsmanship} \
\n\t Quick Synth Control: {self.quick_synth_control} \
\n\t Secret Recipe Book: {self.secret_recipe_book} \
\n\t Can Quicksynth: {self.can_quick_synth} \
\n\t Can HQ: {self.can_hq} \
\n\t EXP Rewarded: {self.exp_rewarded} \
\n\t Status Required: {self.status_required} \
\n\t Item Required: {self.item_required} \
\n\t Is Specialization Required: {self.is_specialization_required} \
\n\t Is Expert: {self.is_expert} \
\n\t Patch Number: {self.patch_number} \
\n\t # Ingredients: {self.num_ingredients} \
\n\t Ingredient Set: {self.ingredients}"