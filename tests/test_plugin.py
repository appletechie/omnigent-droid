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


def test_declares_a_spawn_env_builder() -> None:
    """
    Without a builder the per-session model override is silently dropped.

    Core's ``_build_spawn_env_from_spec`` returns ``None`` for a harness with
    no registered builder, and the ``/model`` override it applies afterwards is
    gated on ``env is not None`` — so the picker's choice never reached
    ``HARNESS_DROID_MODEL`` and every session ran on droid's own default.
    """
    contribution = get_contribution()
    builder = contribution.spawn_env_builders[DROID_KEY]
    assert builder.startswith("omnigent.community.harness.")
    # Core imports it lazily by path; a typo here fails only at session launch.
    from omnigent.harness_plugins import load_object

    assert callable(load_object(builder))


def test_spawn_env_builder_maps_model_and_cwd() -> None:
    """The builder emits the env vars the droid wrap actually reads."""
    from pathlib import Path

    from omnigent.community.harness.droid.spawn_env import build_spawn_env

    class _Executor:
        model = "grok-4.5"
        config: dict[str, object] = {}

    class _Spec:
        executor = _Executor()
        os_env = None

    env = build_spawn_env(_Spec(), cwd=Path("/tmp/ws"))
    assert env["HARNESS_DROID_MODEL"] == "grok-4.5"
    assert env["HARNESS_DROID_CWD"] == "/tmp/ws"
