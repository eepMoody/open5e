import uuid
from django.db import models

# Create your models here.
class Document(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1)
    title = models.TextField() # System Reference Document
    desc = models.TextField() 
    license = models.TextField() # Open Gaming License
    author = models.TextField() # Mike Mearls, Jeremy Crawford, Chris Perkins, Rodney Thompson, Peter Lee, James Wyatt, Robert J. Schwalb, Bruce R. Cordell, Chris Sims, and Steve Townshend, based on original material by E. Gary Gygax and Dave Arneson.
    organization = models.TextField() # Wizards of the Coast
    version = models.TextField() # 5.1
    url = models.URLField() # http://dnd.wizards.com/articles/features/systems-reference-document-srd
    created_at = models.DateTimeField(auto_now_add=True)

class GameContent(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, primary_key=True) # dispel-evil-and-good
    name = models.TextField() # Barbarian or Blinded
    desc = models.TextField() # A description of the Game Content Item
    document = models.ForeignKey(Document, on_delete=models.CASCADE) # Like the System Reference Document
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        abstract=True

class Monster(GameContent):
    size = models.TextField()
    type = models.TextField()
    subtype = models.TextField()
    alignment = models.TextField()
    armor_class = models.IntegerField(default=12)
    hit_points = models.IntegerField(null=True)
    hit_dice = models.TextField()
    speed = models.TextField()
    strength = models.IntegerField(null=True)
    dexterity = models.IntegerField(null=True)
    constitution = models.IntegerField(null=True)
    intelligence = models.IntegerField(null=True)
    wisdom = models.IntegerField(null=True)
    charisma = models.IntegerField(null=True)
    constitution_save = models.IntegerField(null=True)
    intelligence_save = models.IntegerField(null=True)
    wisdom_save = models.IntegerField(null=True)
    perception = models.IntegerField(null=True)
    damage_vulnerabilities = models.TextField()
    damage_resistances = models.TextField()
    damage_immunities = models.TextField()
    condition_immunities = models.TextField()
    senses = models.TextField()
    languages = models.TextField()
    challenge_rating = models.TextField()
    # special_abilities
    # actions
    # legendary_actions
    
    @property
    def get_url(self):
        return "/monsters/%s/" % self.slug

class Spell(GameContent):
    higher_level = models.TextField()
    page = models.TextField()
    range = models.TextField()
    components = models.TextField()
    material = models.TextField()
    ritual = models.TextField()
    duration = models.TextField()
    concentration = models.TextField()
    casting_time = models.TextField()
    level = models.TextField()
    school = models.TextField()
    dnd_class = models.TextField()
    archetype = models.TextField()
    circles = models.TextField()
    
    @property
    def get_url(self):
        return "/spells/%s/" % self.slug

class CharClass(GameContent):
    hit_dice = models.TextField()
    hp_at_1st_level = models.TextField()
    hp_at_higher_levels = models.TextField()
    prof_armor = models.TextField()
    prof_weapons = models.TextField()
    prof_tools = models.TextField()
    prof_saving_throws = models.TextField()
    prof_skills = models.TextField()
    equipment = models.TextField()
    table = models.TextField()
    spellcasting_ability = models.TextField()
    subtypes = models.TextField()

class Archetype(GameContent):
    char_class = models.ForeignKey(CharClass, on_delete=models.CASCADE, null=True)

class Race(GameContent):
    asi_desc = models.TextField()
    asi = models.TextField()
    age = models.TextField()
    alignment = models.TextField()
    size = models.TextField()
    speed = models.TextField()
    speed_desc = models.TextField()
    languages = models.TextField()
    vision = models.TextField()
    traits = models.TextField()
    subtypes = models.TextField()

class SubRace(GameContent):
    asi_desc = models.TextField()
    asi = models.TextField()
    traits = models.TextField()
    parent_race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True)

class Plane(GameContent):
    pass
    
    @property
    def get_url(self):
        return "/planes/%s/" % self.slug

class Section(GameContent):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    
    @property
    def get_url(self):
        return "/sections/%s/" % self.slug
    
class Feat(GameContent):
        
    prerequisite = models.TextField()
    
    @property
    def get_url(self):
        return "/conditions/%s/" % self.slug

class Condition(GameContent):
    pass
    
    @property
    def get_url(self):
        return "/conditions/%s/" % self.slug

class Background(GameContent):
    skill_proficiencies = models.TextField()
    languages = models.TextField()
    equipment = models.TextField()
    feature = models.TextField()
    suggested_characteristics = models.TextField()
    
    @property
    def get_url(self):
        return "/backgrounds/%s/" % self.slug
