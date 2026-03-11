# Quick guide

```{eval-rst}
If you have a a list of USAS semantic tags in a String like so it will validate that they follow the USAS semantic tag schema and return them as a :py:class:`list` of :py:class:`usas_validator.usas_tag.USASTagGroup`:
```

``` python
from usas_validator import utils
usas_tag_string = "Z2/S2mf E3-"
usas_tag_groups = utils.parse_usas_token_group(usas_tag_string)
for usas_token_group in usas_tag_groups:
  print(usas_token_group)
  print()
```

Output:
``` bash
tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False), USASTag(tag='S2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=True, male=True, antecedents=False, neuter=False, idiom=False)]

tags=[USASTag(tag='E3', number_positive_markers=0, number_negative_markers=1, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]
```

You can also load all the USAS tags and their descriptions like so:
``` python
from usas_validator import utils
for usas_tag, tag_description in utils.load_usas_mapper(None, None).items():
  print(f"Tag: {usas_tag}   Description: {tag_description}")
```

The output is long thus only showing the first 5 tags:

``` bash
Tag: A1.1.1   Description: title: General actions, making etc. description: General/abstract terms relating to an activity/action (e.g. act, adventure, approach, arise); a characteristic/feature (e.g. absorb, attacking, automatically); aconstruction/craft and/or the action of constructing/crafting (e.g. arrange, assemble, bolts, boring, break)
Tag: A1.1.2   Description: title: Damaging and destroying description: General/abstract terms depicting damage/destruction/demolition/pollution, etc
Tag: A1.2   Description: title: Suitability description: General/abstract terms relating to appropriateness, suitability, aptness, etc
Tag: A1.3   Description: title: Caution description: General/abstract terms relating to vigilance/care/prudence, or the lack of.
Tag: A1.4   Description: title: Chance, luck description: General/abstract terms depicting likelihood/probability/providence, or the lack of.
```