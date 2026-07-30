"""Entry point Omnigent calls to register the Droid harness.

Discovered through the ``omnigent.community.harness`` entry-point group; core
imports this module during plugin discovery and merges the returned
:class:`HarnessContribution` into its registry.

Deliberately imports nothing but the contribution types: discovery happens at
startup for every installed plugin, so pulling the executor (and through it the
ACP/os_env stack) in here would cost every Omnigent process the import even
when no session ever selects Droid. ``harness_modules`` names the module as a
string so core imports it lazily, on first launch.
"""

from __future__ import annotations

from omnigent.harness_capabilities import (
    AuthModel,
    EffortFamily,
    Elicitation,
    HarnessCapabilities,
    IntegrationMode,
    ModelFamily,
    Resume,
)
from omnigent.harness_install_spec import HarnessInstallSpec
from omnigent.harness_plugins import HarnessContribution

#: Harness id and install key. Droid has no native TUI spelling — the headless
#: ACP surface is the only one — so a single key gates it.
DROID_KEY = "droid"

#: Distribution name, surfaced by core when a spec names ``droid`` but the
#: plugin isn't installed ("pip install omnigent-droid").
DISTRIBUTION = "omnigent-droid"


def get_contribution() -> HarnessContribution:
    """Return the Droid harness registration.

    :returns: The contribution core merges into its harness registry.
    """
    return HarnessContribution(
        name=DISTRIBUTION,
        valid_harnesses=frozenset({DROID_KEY}),
        harness_modules={
            DROID_KEY: "omnigent.community.harness.droid.inner.droid_harness",
        },
        install_specs={
            # Factory ships Droid through a curl installer (no npm) and
            # authenticates with its own configuration — a FACTORY_API_KEY env
            # var or the droid login flow — so Omnigent manages no credential.
            DROID_KEY: HarnessInstallSpec(
                "Droid",
                "droid",
                package=None,
                install_hint="curl -fsSL https://app.factory.ai/cli | sh",
            ),
        },
        # Binary-gated readiness: with install metadata registered, core gates
        # on the droid binary rather than failing open. Auth state is Droid's
        # own and surfaces at the first turn.
        harness_install_keys={DROID_KEY: DROID_KEY},
        # Without this, core's _build_spawn_env_from_spec returns None for
        # droid and the per-session /model override — gated on a non-None env —
        # never reaches HARNESS_DROID_MODEL.
        spawn_env_builders={
            DROID_KEY: "omnigent.community.harness.droid.spawn_env:build_spawn_env",
        },
        model_env_keys={DROID_KEY: "HARNESS_DROID_MODEL"},
        missing_install_package={DROID_KEY: DISTRIBUTION},
        harness_labels={DROID_KEY: "Droid"},
        capabilities={
            DROID_KEY: HarnessCapabilities(
                IntegrationMode.ACP_SUBPROCESS,
                Elicitation.SSE_PERMISSION,
                Resume.COLD_ONLY,
                EffortFamily.NONE,
                ModelFamily.MULTI,
                AuthModel.OWN_AUTH,
                subagents=False,
                interrupt=True,
                streaming=True,
            ),
        },
    )
