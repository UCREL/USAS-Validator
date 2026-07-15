import re
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml

from usas_validator.usas_tag import USASTag, USASTagGroup

TAG_RE = re.compile(r"^[A-Z](\d+)((\.\d+)+)?")
PUNCT_RE = re.compile(r"^PUNCT")
DF_RE = re.compile(r"^Df")
POSITIVE_MARKERS_RE = re.compile(r"\++")
NEGATIVE_MARKERS_RE = re.compile(r"\-+")

# A regular expression that was used to capture edge cases in the original
# C version of the USAS tagger:
# ALT_TAG_RE = re.compile(r"^[a-z](\d+)((\.\d+)+)?")

def parse_usas_token_group(usas_tag_group_text: str,
                           strict: bool = False) -> list[USASTagGroup]:
    r"""
    Given a the string that represents the USAS tags whereby each USAS tag is
    separated by whitespace it is converted into a structured format.

    This whitespace separation of USAS tags is the format that is produced by the
    original C version of the USAS tagger when it outputs USAS tags for a given
    token or meaningful word unit like a Multi Word Expression (MWE).

    The whitespace separation can be one or more spaces, i.e. `    ` or ` `

    A USAS tag can be also be `PUNCT` which represents punctuation. It can also be
    represented as `Df` or `Df` with an affix like `+++` or `mf` etc.

    Complex examples of `usas_tag_group_text`:
    `L1 E3- O4.2- X5.2+ A6.2- A1.7- A7- W3 L2 F1 S1.2.4- Z2 Z2/S2mf Z3 O4.3 G1.2 G1.2/S2mf`

    Args:
        usas_tag_group_text: The string that represents the USAS tags
            produced by the USAS tagger for one token.
        strict: If `True`, the function will raise an error if the USAS tags
            within the given text cannot be parsed as a USAS tag (see ValueError below).
            Default `False`.
    Returns:
        list[USASTagGroup]:
            Structured format of the USAS tags that can be parsed from the given text.
            Any text that cannot be parsed as a USAS tag will be ignored and
            therefore can result in returning an empty list.
    Raises:
        ValueError: If `strict` is True and if the USAS tags within the given
            text cannot be parsed as a USAS tag, whereby each USAS tag after
            whitespace and `/` split should match the following regex:
            `[A-Z](\d+)((\.\d+)+)?`, `Df`, or `PUNCT`.
    Examples:
        >>> from usas_validator.utils import parse_usas_token_group
        >>> usas_token_groups = parse_usas_token_group("Z2/S2mf Z3")
        >>> for usas_token_group in usas_token_groups:
        ...     print(usas_token_group)
        tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False), USASTag(tag='S2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=True, male=True, antecedents=False, neuter=False, idiom=False)]
        tags=[USASTag(tag='Z3', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]

        When using `strict=True`:

        >>> from usas_validator.utils import parse_usas_token_group
        >>> parse_usas_token_group("Invalid", strict=True)
        Traceback (most recent call last):
            ...
        ValueError: Cannot find the tag for this USAS tag text: Invalid

        When using `strict=False` (default) you can ignore invalid USAS tags within the text you are parsing,
        in the example below `Z1` and `Z2` are parsed successfully while `NONE` is ignored:

        >>> from usas_validator.utils import parse_usas_token_group
        >>> parse_usas_token_group("Z1/NONE Z2", strict=False)
        [USASTagGroup(tags=[USASTag(tag='Z1', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]), USASTagGroup(tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)])]
    """

    def parse_usas_tag(usas_tag_text: str,
                       strict: bool) -> USASTag:
        r"""
        Given a single USAS tag text, e.g. `X5.2+` it is converted into
        a structured format.

        Note: a USAS tag text should not contain a `/`,
        e.g. `G1.2/S2mf` as this contains two USAS tags that represent
        a combined semantic meaning of a token.

        Args:
            usas_tag_text: Single USAS tag text
            strict: If `True`, the function will raise an error if the USAS tag
                cannot be parsed as a USAS tag (see ValueError below).
                Default False.
        Returns:
            USASTag:
                A structured format of the USAS tag. If `strict` is `False`
                and the USAS tag cannot be parsed as a USAS tag, then an empty
                `USASTag(tag='')` is returned.
        Raises:
            ValueError: If `strict` is `True` and if it cannot match the given
                text with the USAS tag regex, which is:
                `[A-Z](\d+)((\.\d+)+)?`, `Df`, or `PUNCT`.
        """

        tag_match = TAG_RE.match(usas_tag_text)
        punct_match = PUNCT_RE.match(usas_tag_text)
        df_match = DF_RE.match(usas_tag_text)
        tag = ""

        
        if tag_match:
            tag = tag_match.group()
            usas_tag_text = TAG_RE.sub("", usas_tag_text)
        elif punct_match:
            tag = punct_match.group()
            usas_tag_text = PUNCT_RE.sub("", usas_tag_text)
        elif df_match:
            tag = df_match.group()
            usas_tag_text = DF_RE.sub("", usas_tag_text)
        else:
            if strict:
                raise ValueError(
                    f"Cannot find the tag for this USAS tag text: {usas_tag_text}"
                )
            else:
                return USASTag(tag="")

        number_positive_markers = 0
        positive_marker_match = POSITIVE_MARKERS_RE.search(usas_tag_text)
        if positive_marker_match:
            number_positive_markers = len(positive_marker_match.group())
            usas_tag_text = POSITIVE_MARKERS_RE.sub("", usas_tag_text)

        number_negative_markers = 0
        negative_marker_match = NEGATIVE_MARKERS_RE.search(usas_tag_text)
        if negative_marker_match:
            number_negative_markers = len(negative_marker_match.group())
            usas_tag_text = NEGATIVE_MARKERS_RE.sub("", usas_tag_text)

        is_male = False
        if "m" in usas_tag_text:
            is_male = True

        is_female = False
        if "f" in usas_tag_text:
            is_female = True

        contain_rare_marker_1 = False
        if "%" in usas_tag_text:
            contain_rare_marker_1 = True

        contain_rare_marker_2 = False
        if "@" in usas_tag_text:
            contain_rare_marker_2 = True

        contains_antecedent = False
        if "c" in usas_tag_text:
            contains_antecedent = True

        contains_neuter = False
        if "n" in usas_tag_text:
            contains_neuter = True

        # Currently do not support finding idioms
        is_idiom = False

        return USASTag(
            tag=tag,
            male=is_male,
            female=is_female,
            rarity_marker_1=contain_rare_marker_1,
            rarity_marker_2=contain_rare_marker_2,
            number_positive_markers=number_positive_markers,
            number_negative_markers=number_negative_markers,
            antecedents=contains_antecedent,
            neuter=contains_neuter,
            idiom=is_idiom,
        )

    token_usas_tags: list[USASTagGroup] = []

    for usas_tag_group in re.findall(r"\S+", usas_tag_group_text):
        usas_tags: list[USASTag] = []
        for usas_tag_text in usas_tag_group.split("/"):
            parsed_usas_tag = parse_usas_tag(usas_tag_text, strict=strict)
            if parsed_usas_tag.tag == "":
                continue
            usas_tags.append(parsed_usas_tag)
        if usas_tags:
            token_usas_tags.append(USASTagGroup(tags=usas_tags))

    return token_usas_tags


def load_usas_mapper(usas_tag_descriptions_file: Path | None,
                     tags_to_filter_out: set[str] | None
                     ) -> dict[str, str]:
    """
    Returns a dictionary of USAS tags and their descriptions.

    Args:
        usas_tag_descriptions_file: The path to the YAML file that
            contains the USAS tags and their descriptions. If None then the
            function will use the USAS tags and description file that is located
            within the package at `usas_csv_auto_labeling/data/usas/usas_mapper.yaml`.
        tags_to_filter_out: A set of USAS tags to filter out.

    Returns:
        dict[str, str]: A dictionary of USAS tags and their descriptions.
    
    Raises:
        FileNotFoundError: If the `usas_tag_descriptions_file` is not found.
        ValueError: If the `usas_tag_descriptions_file` is not a file.

    Examples:
        >>> from usas_validator.utils import load_usas_mapper
        >>> usas_tag_descriptions = load_usas_mapper(None, None)
        >>> usas_tag_descriptions["X1"]
        'title: General description: General terms relating to psychological actions, states and processes'
    """

    def _get_usas_tag_descriptions(usas_tag_name: str,
                                   usas_tag_dict: dict[str, Any],
                                   collected_tag_descriptions: dict[str, str]
                                   ) -> dict[str, str]:
        """
        A recursive function that loops through the `usas_tag_dict` and returns a
        dictionary of the USAS tag and as a value it's description. Each USAS tag
        that is found is added to the `collected_tag_descriptions` dictionary.
        Once all the USAS tags are found, the `collected_tag_descriptions` is
        returned.

        The description is made of the USAS tag title and description in the
        following format: `title: <title> description: <description>`

        Args:
            usas_tag_name: The name of the USAS tag.
            usas_tag_dict: A dictionary containing the raw
                USAS tag data that is read from the YAML file.
            collected_tag_descriptions: A dictionary of all
                USAS tags and their descriptions.

        Returns:
            dict[str, str]: A dictionary of USAS tags and their descriptions.
        """
        if "title" in usas_tag_dict and "description" in usas_tag_dict:
            title_description = f"title: {usas_tag_dict['title']} description: {usas_tag_dict['description']}"
            if usas_tag_name in collected_tag_descriptions:
                raise KeyError(f"Duplicate usas tag name found: {usas_tag_name} "
                               "when reading the following data: "
                               f"{usas_tag_dict}, currently found usas tags: "
                               f"{collected_tag_descriptions}")
            collected_tag_descriptions[usas_tag_name] = title_description.strip()
        elif "title" in usas_tag_dict:
            raise KeyError("No description key found when it is expected for: "
                           f"{usas_tag_name} {usas_tag_dict}")
        elif "description" in usas_tag_dict:
            raise KeyError("No title key found when it is expected for: "
                           f"{usas_tag_name} {usas_tag_dict}")

        keys_to_ignore = set(["title", "description"])
        for child_usas_tag_name, child_usas_tag_dict in usas_tag_dict.items():
            if child_usas_tag_name not in keys_to_ignore:
                collected_tag_descriptions = _get_usas_tag_descriptions(child_usas_tag_name,
                                                                          child_usas_tag_dict,
                                                                                        collected_tag_descriptions)
        return collected_tag_descriptions

    usas_tag_descriptions_file_path: Path = Path()
    if usas_tag_descriptions_file is None:
        usas_tag_descriptions_file_str = str(files("usas_validator").joinpath("data/usas/usas_mapper.yaml"))
        usas_tag_descriptions_file_path = Path(usas_tag_descriptions_file_str)
    else:
        usas_tag_descriptions_file_path = usas_tag_descriptions_file

    if usas_tag_descriptions_file_path.exists() is False:
        raise FileNotFoundError(f"USAS tag descriptions file not found at: "
                                f"{usas_tag_descriptions_file_path}")
    elif usas_tag_descriptions_file_path.is_file() is False:
        raise ValueError(f"USAS tag descriptions file is not a file: "
                         f"{usas_tag_descriptions_file_path}")

    usas_mapping: dict[str, str] = {}
    with usas_tag_descriptions_file_path.open("r") as usas_mapper_fp:
        usas_mapping_data = usas_mapper_fp.read()
        for high_level_usas_tag, high_level_usas_tag_dict in yaml.safe_load(usas_mapping_data).items():
            usas_mapping = _get_usas_tag_descriptions(high_level_usas_tag,
                                                      high_level_usas_tag_dict,
                                                      usas_mapping)
    if tags_to_filter_out:
        tmp_usas_mapping = {}
        for key, value in usas_mapping.items():
            if key in tags_to_filter_out:
                continue
            tmp_usas_mapping[key] = value
        usas_mapping = tmp_usas_mapping
    return usas_mapping


def keep_valid_usas_tags(usas_tag_string: str, valid_usas_tags: set[str]) -> list[USASTagGroup]:
    """
    Filter a USAS tag string to only include tags present in a given set of valid tags.

    Parses the input string into :class:`~usas_validator.usas_tag.USASTagGroup` objects (in non-strict mode,
    so malformed tags are skipped rather than raising errors), then removes any
    individual :class:`~usas_validator.usas_tag.USASTag` whose base tag is not in ``valid_usas_tags``.
    Tag groups that become empty after filtering are dropped entirely.

    Args:
        usas_tag_string: A space-separated string of USAS tag groups, e.g. ``"Z2/S2mf E3-"``.
        valid_usas_tags: A set of acceptable base USAS tag strings (e.g. ``{"Z2", "E3"}``).
            Typically obtained from :func:`~usas_validator.utils.load_usas_mapper`.

    Returns:
        A list of :class:`~usas_validator.usas_tag.USASTagGroup` objects containing only tags whose base
        tag appears in ``valid_usas_tags``. Groups with no remaining valid tags
        are excluded.

    Examples:
        >>> from usas_validator.utils import keep_valid_usas_tags
        >>> valid = {"Z2", "E3"}
        >>> keep_valid_usas_tags("Z2/S2mf E3-", valid)
        [USASTagGroup(tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]), USASTagGroup(tags=[USASTag(tag='E3', number_positive_markers=0, number_negative_markers=1, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)])]

        >>> keep_valid_usas_tags("Z2/S2mf E3-", {"Z2"})
        [USASTagGroup(tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)])]
    """
    all_valid_usas_tag_groups = parse_usas_token_group(usas_tag_string, strict=False)
    filtered_usas_tag_groups = []
    for usas_tag_group in all_valid_usas_tag_groups:
        filtered_usas_tags = [usas_tag for usas_tag in usas_tag_group.tags
                                             if usas_tag.tag in valid_usas_tags]
        if filtered_usas_tags:
            filtered_usas_tag_groups.append(USASTagGroup(tags=filtered_usas_tags))
    return filtered_usas_tag_groups


def mwe_token_indexes_from_slices(mwe_index_slices: list[tuple[int, int]]) -> frozenset[int]:
    """
    Expand a list of Multi Word Expression (MWE) index slices into the individual
    token indexes they cover.

    Each tuple is a `(start, end)` slice, with `end` exclusive, in the same way as
    the built-in :class:`range` callable, e.g. `(2, 5)` covers indexes `2`, `3`, and `4`. A single
    token MWE is therefore represented as `(i, i + 1)`, which expands to just `i`.

    Args:
        mwe_index_slices: A list of `(start, end)` tuples, one per MWE, where
            `end` is exclusive.

    Returns:
        A frozenset of every token index covered by any of the given slices.

    Examples:
        >>> from usas_validator.utils import mwe_token_indexes_from_slices
        >>> sorted(mwe_token_indexes_from_slices([(2, 5)]))
        [2, 3, 4]

        A single token MWE, represented as `(i, i + 1)`:

        >>> sorted(mwe_token_indexes_from_slices([(0, 1)]))
        [0]

        Multiple, possibly overlapping, MWE slices are merged into one frozenset 
        this can occur with MWEs that are discontinuous:

        >>> sorted(mwe_token_indexes_from_slices([(0, 2), (1, 3), (5, 6)]))
        [0, 1, 2, 5]
    """
    all_mwe_token_indexes = set()
    for mwe_index_range in mwe_index_slices:
        all_mwe_token_indexes.update(range(*mwe_index_range))
    return frozenset(all_mwe_token_indexes)


def mwe_token_labels_from_indexes(mwe_indexes: list[frozenset[int]], number_tokens: int) -> list[set[int]]:
    """
    Represents each MWE as a unique label, ordered by the starting position of its
    first token, the first MWE is labelled 1 and the second 2 and so on. Each token's
    labels are stored at that token's index in the returned list.

    Args:
        mwe_indexes: A list of frozensets of token indexes for each MWE. Every
            frozenset must be non-empty and every index must satisfy
            `0 <= index < number_tokens`. A singleton frozenset, e.g. `{2}`, is
            treated as a single-token MWE (see the single token example below),
            consistent with the `(i, i + 1)` slice convention used by
            :func:`~usas_validator.utils.mwe_token_indexes_from_slices`; this
            function does not distinguish genuine multi-token MWEs from
            single-token ones.
        number_tokens: The number of tokens in the sentence.

    Returns:
        A list, of length `number_tokens`, of sets that contain unique labels, one
        unique label per MWE. A MWE is represented by the tokens that are associated
        with each label. If a token does not belong to a MWE it is represented as an
        empty set.

    Raises:
        ValueError: If any frozenset in `mwe_indexes` is empty, or if any token
            index within `mwe_indexes` is not in the range `0 <= index < number_tokens`.

    Examples:
        >>> from usas_validator.utils import mwe_token_labels_from_indexes
        >>> mwe_token_labels_from_indexes([frozenset({0, 1, 3}), frozenset({2, 3})], 4)
        [{1}, {1}, {2}, {1, 2}]

        When a token in the text does not belong to a MWE it is represented as an empty set:

        >>> from usas_validator.utils import mwe_token_labels_from_indexes
        >>> mwe_token_labels_from_indexes([frozenset({2, 3})], 5)
        [set(), set(), {1}, {1}, set()]

        A singleton frozenset is labelled the same way as any other MWE, even
        though it represents a single token rather than a multi word expression:

        >>> from usas_validator.utils import mwe_token_labels_from_indexes
        >>> mwe_token_labels_from_indexes([frozenset({0}), frozenset({1, 2})], 3)
        [{1}, {2}, {2}]
    """
    for mwe_index in mwe_indexes:
        if not mwe_index:
            raise ValueError("Cannot label an empty MWE, every frozenset in "
                              "`mwe_indexes` must contain at least one token index.")
        if min(mwe_index) < 0 or max(mwe_index) >= number_tokens:
            raise ValueError(f"MWE token indexes {mwe_index} are not all within "
                              f"range 0 <= index < number_tokens ({number_tokens}).")

    # Determine the starting position of the first token for each MWE.
    mwe_indexes_with_min_index: list[tuple[frozenset[int], int]] = [(mwe_index, min(mwe_index)) for mwe_index in mwe_indexes]

    # Sort the MWEs by starting position.
    mwe_indexes_with_min_index.sort(key=lambda mwe_index_with_min_index: mwe_index_with_min_index[1])

    # Assign unique labels to the MWEs.
    mwe_labels: list[set[int]] = [set() for _ in range(number_tokens)]

    for mwe_label, mwe_index_with_min_value in enumerate(mwe_indexes_with_min_index, start=1):
        for mwe_index in mwe_index_with_min_value[0]:
            mwe_labels[mwe_index].add(mwe_label)
    return mwe_labels


def mwe_labels_from_pymusas_indexes(pymusas_mwe_index_slices: list[list[tuple[int, int]]]) -> list[set[int]]:
    """
    Convert the raw, per-token Multi Word Expression (MWE) index slices produced by
    a PyMUSAS tagger into MWE labels for each token in the sentence.

    For each token, PyMUSAS reports a list of `(start, end)` slices, one per
    token in the MWE it belongs to (more than one slice means the MWE is
    discontinuous), following the same convention as
    :func:`~usas_validator.utils.mwe_token_indexes_from_slices`. Single word
    expressions are reported as a single `(i, i + 1)` slice and are not MWEs,
    so they are filtered out here before labelling the remainder with
    :func:`~usas_validator.utils.mwe_token_labels_from_indexes`.

    Args:
        pymusas_mwe_index_slices: One entry per token in the sentence, in
            token order, each being the list of `(start, end)` MWE index
            slices PyMUSAS reported for that token (e.g. from
            `token._.pymusas_mwe_indexes`).

    Returns:
        A list, of the same length as `pymusas_mwe_index_slices`, of sets
        that contain unique MWE labels per token, as returned by
        :func:`~usas_validator.utils.mwe_token_labels_from_indexes`. Tokens
        that are not part of a MWE are represented as an empty set.

    Examples:
        >>> from usas_validator.utils import mwe_labels_from_pymusas_indexes
        >>> mwe_labels_from_pymusas_indexes([[(0, 2)], [(0, 2)], [(2, 3)]])
        [{1}, {1}, set()]

        Single token expressions, represented as `(i, i + 1)`, are not MWEs
        and are therefore not labelled:

        >>> from usas_validator.utils import mwe_labels_from_pymusas_indexes
        >>> mwe_labels_from_pymusas_indexes([[(0, 1)], [(1, 2)]])
        [set(), set()]

        Discontinuous MWEs report more than one slice per token, but still
        resolve to a single label:

        >>> from usas_validator.utils import mwe_labels_from_pymusas_indexes
        >>> mwe_labels_from_pymusas_indexes(
        ...     [[(0, 1), (2, 3)], [(1, 2)], [(0, 1), (2, 3)]]
        ... )
        [{1}, set(), {1}]
    """
    unique_mwe_indexes: set[frozenset[int]] = set()
    for token_mwe_index_slices in pymusas_mwe_index_slices:
        token_mwe_indexes = mwe_token_indexes_from_slices(token_mwe_index_slices)
        if len(token_mwe_indexes) > 1:
            unique_mwe_indexes.add(token_mwe_indexes)

    return mwe_token_labels_from_indexes(list(unique_mwe_indexes),
                                        number_tokens=len(pymusas_mwe_index_slices))