from usas_validator.usas_tag import USASTag, USASTagGroup


def test_tag_strings() -> None:
    """Test the USASTagGroup.tag_strings property."""

    # Test a group with a single tag.
    group = USASTagGroup(tags=[USASTag(tag="A1.1.1")])
    assert group.tag_strings == ["A1.1.1"]

    # Test a group with multiple tags, markers should not affect the
    # returned tag strings.
    group = USASTagGroup(tags=[
        USASTag(tag="E2", number_negative_markers=1),
        USASTag(tag="S7.1", number_positive_markers=1)
    ])
    assert group.tag_strings == ["E2", "S7.1"]

    # Test a group with no tags.
    group = USASTagGroup(tags=[])
    assert group.tag_strings == []
