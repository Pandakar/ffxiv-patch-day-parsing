# Object to represent a minified version of an FFXIV Item.
# Only displaying the stuff we actually care about, basically meta-information.


class Item(object):

    def __init__(self):
        # for now. acknowledging fields then we'll filter down to what we actually want
        self.key = -1                   #   -1
        self.name = ""                  #    9
        self.level_item = ""            #   11
        self.item_search_category = ""  #   16
        self.stack_size = ""            #   19
        self.is_unique = ""             #   20
        self.is_untradable = ""         #   21
        self.is_indisposable = ""       #   22
        self.can_be_hq = ""             #   25
        self.is_collectable = ""        #   34
        self.always_collectable = ""    #   35
        self.level_equip = ""           #   37
        self.equip_restriction = ""     #   38
        self.class_job_category = ""    #   39

    def __repr__(self):
        return_string = F"{self.key} \
\n\tName: {self.name} \
\n\tLevel Item: {self.level_item} \
\n\tItem Search Category: {self.item_search_category} \
\n\tStack Size: {self.stack_size} \
\n\tIs Unique: {self.is_unique} \
\n\tIs Untradable: {self.is_untradable} \
\n\tIs Indisposable: {self.is_indisposable} \
\n\tCan be HQ: {self.can_be_hq} \
\n\tIs Collectable: {self.is_collectable} \
\n\tAlways Collectable: {self.always_collectable} \
\n\tLevel Equip: {self.level_equip} \
\n\tEquip Restriction: {self.equip_restriction} \
\n\tClass Job Category: {self.class_job_category}"

        return return_string

    def to_sheet_row(self):
        '''
        wrapper to help convert to a list
        '''
        return list(self.__dict__.values())