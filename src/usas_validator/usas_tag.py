from typing import Literal

from pydantic import BaseModel, Field


class USASTag(BaseModel):
    """
    Represents all of the properties associated with a USAS tag.
    """

    tag: str = Field(title="USAS Tag", description="USAS Tag", examples=["A1.1.1"])
    """
    The USAS tag.
    """
    
    number_positive_markers: int = Field(
        0,
        title="Positive Markers",
        description="Number of positive markers.",
        examples=[0, 1, 2, 3],
    )
    """
    The number of positive markers.
    """

    number_negative_markers: int = Field(
        0,
        title="Negative Markers",
        description="Number of negative markers.",
        examples=[0, 1, 2, 3],
    )
    """
    The number of negative markers.
    """

    rarity_marker_1: bool = Field(
        False, title="Rare Marker 1", description="Rarity marker 1 indicated by %"
    )
    """
    True if the USAS tag contains the rarity marker %.
    """

    rarity_marker_2: bool = Field(
        False, title="Rare Marker 2", description="Rarity marker 2 indicated by @"
    )
    """
    True if the USAS tag contains the rarity marker @.
    """

    female: bool = Field(False, title="Female", description="Female")
    """
    True if the USAS tag contains the female marker denoted by `f`.
    """

    male: bool = Field(False, title="Male", description="Male")
    """
    True if the USAS tag contains the male marker denoted by `m`.
    """

    antecedents: bool = Field(
        False,
        title="Antecedents",
        description="Potential antecedents of conceptual anaphors (neutral for number)",
    )
    """
    True if the USAS tag contains the antecedents marker denoted by `c`.
    """

    neuter: bool = Field(False, title="Neuter", description="Neuter")
    """
    True if the USAS tag contains the neuter marker denoted by `n`.
    """

    idiom: Literal[False] = Field(False, title="Idiom",
                                  description="Is it an idiom, currently not supported and is always False.")
    """
    False, currently not supported and therefore is always False.
    """

class USASTagGroup(BaseModel):
    """
    Represents a grouping of one or more USAS tags that are associated to a
    token.
    """

    _tags_description = (
        "A grouping of one or more USAS tags whereby if more "
        "than one exists then the word is an equal member of "
        "all semantic tags/categories"
    )
    _tags_examples = [
        [USASTag(tag="A1.1.1")],
        [
            USASTag(tag="E2", number_negative_markers=1),
            USASTag(tag="S7.1", number_positive_markers=1),
        ],
    ]
    tags: list[USASTag] = Field(
        title="USAS Tags", description=_tags_description, examples=_tags_examples
    )
    """
    A list of USAS tags that are associated to a token. This grouping
        of USAS tags is a way of representing multi tag membership.
    """