"""The contribution this plugin exports must satisfy core's plugin contract.

These are the checks core runs at discovery time (namespace placement, no
builtin-name collisions, no native terminal metadata). Asserting them here
means a packaging mistake fails in this repo's CI rather than silently
disabling the harness in someone's Omnigent install.
"""

from __future__ import annotations

from omnigent.community.harness.droid.plugin import DROID_KEY, get_contribution


def test_contribution_registers_the_droid_harness() -> None:
    contribution = get_contribution()
    assert contribution.name == "omnigent-droid"
    assert contribution.valid_harnesses == frozenset({DROID_KEY})
    assert contribution.harness_labels[DROID_KEY] == "Droid"


def test_harness_module_lives_under_the_community_namespace() -> None:
    """Core rejects a plugin whose modules sit outside its namespace."""
    module = get_contribution().harness_modules[DROID_KEY]
    assert module.startswith("omnigent.community.harness.")


def test_declares_no_native_terminal_metadata() -> None:
    """Community native terminal harnesses are rejected by core.

    Droid is an ACP subprocess, not a TUI wrap, so both must stay empty —
    setting either would make core refuse the whole plugin at load.
    """
    contribution = get_contribution()
    assert contribution.native_harnesses == frozenset()
    assert contribution.native_agents == ()


def test_install_metadata_makes_readiness_binary_gated() -> None:
    """Without an install key core fails open and reports Droid always ready."""
    contribution = get_contribution()
    assert contribution.harness_install_keys[DROID_KEY] == DROID_KEY
    spec = contribution.install_specs[DROID_KEY]
    assert spec.binary == "droid"
    # Factory ships a curl installer, not a package Omnigent can install.
    assert spec.package is None


def test_core_accepts_the_contribution() -> None:
    """Run core's own validator rather than trusting the shape by eye."""
    from omnigent.harness_plugins import _validate_community_contribution

    assert (
        _validate_community_contribution(
            get_contribution(),
            entry_point_name="droid",
            existing=(),
        )
        is None
    )
