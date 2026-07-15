# Quick guide

```{eval-rst}
If you have a a list of USAS semantic tags in a String like so it will validate that they follow the USAS semantic tag schema and return them as a :class:`list` of :class:`usas_validator.usas_tag.USASTagGroup`:
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

```{eval-rst}
If you only want to keep tags that are known/valid (e.g. from a set of tags you trust or that came from :func:`usas_validator.utils.load_usas_mapper`), you can filter a USAS tag string down to just those tags:
```

``` python
from usas_validator import utils
usas_tag_string = "Z2/S2mf E3-"
valid_usas_tags = {"Z2", "E3"}
usas_tag_groups = utils.keep_valid_usas_tags(usas_tag_string, valid_usas_tags)
for usas_token_group in usas_tag_groups:
  print(usas_token_group)
  print()
```

Output:
``` bash
tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]

tags=[USASTag(tag='E3', number_positive_markers=0, number_negative_markers=1, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]
```

Notice that `S2mf` was dropped from the first group as `S2` is not in `valid_usas_tags`, but as `Z2` was still valid the group is kept. If every tag in a group is filtered out, the whole group is dropped from the result.

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

```{eval-rst}
Multi Word Expressions (MWEs), like ``New York``, are often represented as a ``(start, end)`` slice per MWE, where ``end`` is exclusive in the same way as the builtin :class:`range` callable. :func:`usas_validator.utils.mwe_token_indexes_from_slices` expands a slice into the individual token indexes it covers, and :func:`usas_validator.utils.mwe_token_labels_from_indexes` then assigns each token a unique label per MWE, which is useful for telling which tokens belong together once you already have their per-token USAS tags:
```

``` python
from usas_validator import utils

# Tokens: The(0) New(1) York(2) Times(3) reported(4) news(5)
# Two MWEs: "New York" (tokens 1-2) and "reported news" (tokens 4-5)
mwe_slices = [(1, 3), (4, 6)]

mwe_indexes = [utils.mwe_token_indexes_from_slices([mwe_slice]) for mwe_slice in mwe_slices]
print(mwe_indexes)

mwe_labels = utils.mwe_token_labels_from_indexes(mwe_indexes, number_tokens=6)
print(mwe_labels)
```

Output:
``` bash
[frozenset({1, 2}), frozenset({4, 5})]
[set(), {1}, {1}, set(), {2}, {2}]
```

Each set in `mwe_labels` corresponds to the token at that index: an empty set means the token isn't part of any MWE, and a set with more than one label means the token belongs to more than one, overlapping or discontinuous, MWE.

```{eval-rst}
Neither function distinguishes a genuine multi-token MWE from a single token: a ``(i, i + 1)`` slice, e.g. ``(0, 1)``, is expanded by :func:`usas_validator.utils.mwe_token_indexes_from_slices` into the singleton frozenset ``frozenset({0})``, and :func:`usas_validator.utils.mwe_token_labels_from_indexes` will happily assign that singleton its own label, the same as any other MWE:
```

``` python
from usas_validator import utils

# Tokens: The(0) cat(1) sat(2)
# "The" (token 0) is passed in as if it were a single-token MWE, and "cat sat" (tokens 1-2) is a genuine MWE
mwe_slices = [(0, 1), (1, 3)]

mwe_indexes = [utils.mwe_token_indexes_from_slices([mwe_slice]) for mwe_slice in mwe_slices]
print(mwe_indexes)

mwe_labels = utils.mwe_token_labels_from_indexes(mwe_indexes, number_tokens=3)
print(mwe_labels)
```

Output:
``` bash
[frozenset({0}), frozenset({1, 2})]
[{1}, {2}, {2}]
```

If you only want to label genuine multi-token MWEs, filter `mwe_indexes` to entries with more than one token index (`len(mwe_index) > 1`) before calling `mwe_token_labels_from_indexes`.