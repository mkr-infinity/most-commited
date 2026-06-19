#!/usr/bin/env python3
"""
Bulk Commit Generator v1.0
~~~~~~~~~~~~~~~~~~~~~~~~~~

A professional, production-ready CLI tool for generating real Git commits
with actual file changes, supporting signed and unsigned commits.

Repository: https://github.com/mkr-infinity/most-commited
Author:     Mohammad Kaif Raja (mkr-infinity)
Copyright:  Copyright (c) 2026 Mohammad Kaif Raja. All Rights Reserved.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~  If you modify, redistribute, fork, or reuse this project, please       ~
~  provide proper credit to Mohammad Kaif Raja (mkr-infinity).            ~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
Unauthorized removal of attribution is strictly prohibited.
"""

from __future__ import annotations

import os
import sys
import subprocess
import random
import time
from datetime import datetime
from typing import Optional, Tuple


def ensure_python_dependency(package: str, import_name: Optional[str] = None) -> None:
    """Install a required Python dependency before importing it.

    The script is intentionally self-contained, so a missing UI dependency should
    be fixed automatically instead of crashing with ModuleNotFoundError.
    """
    module_name = import_name or package
    try:
        __import__(module_name)
        return
    except ImportError:
        pass

    print(f"Installing missing dependency: {package}")
    install_attempts = [
        [sys.executable, "-m", "pip", "install", "--user", package],
        [sys.executable, "-m", "pip", "install", "--break-system-packages", package],
    ]

    last_error = ""
    for command in install_attempts:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=180,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            last_error = str(exc)
            continue
        if result.returncode == 0:
            try:
                __import__(module_name)
                print(f"Installed dependency successfully: {package}")
                return
            except ImportError as exc:
                last_error = str(exc)
                continue
        last_error = result.stderr.strip() or result.stdout.strip()

    print(f"Could not install required dependency: {package}")
    print(last_error)
    print(f"Install it manually with: {sys.executable} -m pip install {package}")
    sys.exit(1)


ensure_python_dependency("rich")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    SpinnerColumn,
)
from rich.text import Text
from rich import box
from rich.align import Align
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.theme import Theme
from rich.rule import Rule
from rich.live import Live


# ═════════════════════════════════════════════════════════════════════════ #
#  CONSTANTS & BRANDING                                                    #
# ═════════════════════════════════════════════════════════════════════════ #

VERSION = "v1.0.0"
RELEASE_DATE = "2026-06-19"
BUILD = "Current Release"
AUTHOR = "Mohammad Kaif Raja"
USERNAME = "mkr-infinity"
INSTAGRAM_ID = "mkr_infinity"
GITHUB_LOGO = ""
INSTAGRAM_LOGO = ""
REPOSITORY_URL = "https://github.com/mkr-infinity/most-commited"
GITHUB_URL = "https://github.com/mkr-infinity"
INSTAGRAM_URL = "https://instagram.com/mkr_infinity"
COPYRIGHT = f"Copyright (c) 2026 {AUTHOR}. All Rights Reserved."

DEFAULT_FOLDER = "src"
ACTIVITY_FILE = "activity.log"

# ═════════════════════════════════════════════════════════════════════════ #
#  EMOJI POOL (100+ unique emojis)                                         #
# ═════════════════════════════════════════════════════════════════════════ #

EMOJI_POOL = [
    # Activity & Status
    "\U0001f680",  # 🚀 Rocket
    "\U0001f3af",  # 🎯 Target
    "\U0001f525",  # 🔥 Fire
    "\u2728",      # ✨ Sparkles
    "\U0001f6e0\ufe0f",  # 🛠️ Tools
    "\U0001f4e6",  # 📦 Package
    "\u26a1",      # ⚡ Lightning
    "\U0001f31f",  # 🌟 Star
    "\U0001f389",  # 🎉 Party Popper
    "\u2705",      # ✅ Check Mark
    # Technology & Code
    "\U0001f9e0",  # 🧠 Brain
    "\U0001f4a1",  # 💡 Light Bulb
    "\U0001f4c8",  # 📈 Chart Up
    "\U0001f527",  # 🔧 Wrench
    "\U0001f4dd",  # 📝 Memo
    "\U0001f30d",  # 🌍 Globe
    "\U0001f3c6",  # 🏆 Trophy
    "\U0001f3a8",  # 🎨 Art Palette
    "\U0001f4da",  # 📚 Books
    "\U0001f512",  # 🔒 Lock
    "\U0001f504",  # 🔄 Refresh
    # Development
    "\U0001f4bb",  # 💻 Laptop
    "\U0001f916",  # 🤖 Robot
    "\U0001f50d",  # 🔍 Magnifying Glass
    "\U0001f50e",  # 🔎 Magnifying Glass Right
    "\U0001f4ca",  # 📊 Bar Chart
    "\U0001f4cb",  # 📋 Clipboard
    "\U0001f4cc",  # 📌 Pushpin
    "\U0001f4cd",  # 📍 Round Pushpin
    "\U0001f4ce",  # 📎 Paperclip
    "\U0001f4d0",  # 📐 Triangle Ruler
    # Success & Growth
    "\U0001f31f",  # 🌟 Glowing Star
    "\u2b50",      # ⭐ Star
    "\U0001f947",  # 🥇 Gold Medal
    "\U0001f948",  # 🥈 Silver Medal
    "\U0001f949",  # 🥉 Bronze Medal
    "\U0001f3c5",  # 🏅 Sports Medal
    "\U0001f396\ufe0f",  # 🎖️ Military Medal
    "\U0001f44d",  # 👍 Thumbs Up
    "\U0001f44c",  # 👌 OK Hand
    "\U0001f4af",  # 💯 Hundred Points
    # Objects & Tools
    "\U0001f4e7",  # 📧 Email
    "\U0001f4e8",  # 📨 Incoming Envelope
    "\U0001f4e9",  # 📩 Envelope with Arrow
    "\U0001f4ea",  # 📫 Mailbox
    "\U0001f4eb",  # 📬 Mailbox with Mail
    "\U0001f4ee",  # 📮 Postbox
    "\U0001f4f1",  # 📱 Mobile Phone
    "\U0001f4f7",  # 📷 Camera
    "\U0001f4f8",  # 📸 Camera with Flash
    "\U0001f4fd\ufe0f",  # 📽️ Projector
    # Nature & Environment
    "\U0001f33c",  # 🌼 Blossom
    "\U0001f33a",  # 🌺 Hibiscus
    "\U0001f338",  # 🌸 Cherry Blossom
    "\U0001f33b",  # 🌻 Sunflower
    "\U0001f331",  # 🌱 Seedling
    "\U0001f334",  # 🌴 Palm Tree
    "\U0001f335",  # 🌵 Cactus
    "\U0001f30e",  # 🌎 Globe Americas
    "\U0001f30f",  # 🌏 Globe Asia-Australia
    "\U0001f310",  # 🌐 Globe with Meridians
    # Weather & Elements
    "\u2600\ufe0f",  # ☀️ Sun
    "\U0001f31c",  # 🌜 Moon
    "\u2601\ufe0f",  # ☁️ Cloud
    "\u26c5",      # ⛅ Sun Behind Cloud
    "\U0001f308",  # 🌈 Rainbow
    "\U0001f4a6",  # 💦 Droplets
    "\U0001f4a7",  # 💧 Droplet
    "\U0001f30a",  # 🌊 Water Wave
    "\U0001f525",  # 🔥 Fire
    # Symbols & Signs
    "\u267b\ufe0f",  # ♻️ Recycling
    "\u2699\ufe0f",  # ⚙️ Gear
    "\u2697\ufe0f",  # ⚗️ Alembic
    "\U0001f4e1",  # 📡 Satellite Antenna
    "\U0001f50b",  # 🔋 Battery
    "\U0001f50c",  # 🔌 Electric Plug
    "\U0001f3b5",  # 🎵 Musical Note
    "\U0001f3b6",  # 🎶 Multiple Musical Notes
    "\U0001f3b7",  # 🎷 Saxophone
    "\U0001f3b8",  # 🎸 Guitar
    # Flags & Awards
    "\U0001f3c1",  # 🏁 Chequered Flag
    "\U0001f6a9",  # 🚩 Triangular Flag
    "\U0001f38c",  # 🎌 Crossed Flags
    "\U0001f3f3\ufe0f",  # 🏳️ White Flag
    "\U0001f3f4",  # 🏴 Black Flag
    # Miscellaneous
    "\U0001f4ac",  # 💬 Speech Balloon
    "\U0001f4ad",  # 💭 Thought Balloon
    "\U0001f5e8\ufe0f",  # 🗨️ Left Speech Bubble
    "\U0001f5ef\ufe0f",  # 🗯️ Right Anger Bubble
    "\U0001f4a2",  # 💢 Anger Symbol
    "\U0001f4a3",  # 💣 Bomb
    "\U0001f4a4",  # 💤 Zzz
    "\U0001f4a5",  # 💥 Collision
    "\U0001f4a8",  # 💨 Dashing Away
    "\U0001f4a9",  # 💩 Pile of Poo
    "\U0001f4aa",  # 💪 Flexed Biceps
    # More Tech
    "\U0001f5a5\ufe0f",  # 🖥️ Desktop Computer
    "\U0001f5a8\ufe0f",  # 🖨️ Printer
    "\U0001f5b1\ufe0f",  # 🖱️ Computer Mouse
    "\U0001f5b2\ufe0f",  # 🖲️ Trackball
    "\U0001f4bd",  # 💽 Computer Disk
    "\U0001f4be",  # 💾 Floppy Disk
    "\U0001f4bf",  # 💿 Optical Disk
    "\U0001f4c0",  # 📀 DVD
    "\U0001f3a5",  # 🎥 Movie Camera
    "\U0001f39e\ufe0f",  # 🎞️ Film Frames
]

# ═════════════════════════════════════════════════════════════════════════ #
#  ACTIVITY MESSAGES POOL (200+ messages)                                  #
# ═════════════════════════════════════════════════════════════════════════ #

MESSAGE_POOL = [
    # Repository & Structure
    "Improved repository structure",
    "Enhanced project consistency",
    "Updated development history",
    "Added workflow activity",
    "Improved source organization",
    "Enhanced project metadata",
    "Optimized repository tracking",
    "Refined application workflow",
    "Enhanced code maintainability",
    "Updated project documentation",
    # Code Quality
    "Refactored core modules",
    "Optimized performance bottlenecks",
    "Improved error handling logic",
    "Enhanced type safety across codebase",
    "Reduced technical debt in modules",
    "Improved code coverage metrics",
    "Enhanced logging infrastructure",
    "Optimized data processing pipeline",
    "Refined algorithm efficiency",
    "Cleaned up deprecated methods",
    # Features & Development
    "Added new feature implementation",
    "Enhanced existing functionality",
    "Integrated external API service",
    "Implemented caching mechanism",
    "Added validation logic",
    "Enhanced user authentication flow",
    "Improved data serialization",
    "Added pagination support",
    "Implemented rate limiting",
    "Enhanced search functionality",
    # Testing & Quality
    "Added unit test coverage",
    "Enhanced integration tests",
    "Updated test fixtures",
    "Improved test performance",
    "Added end-to-end testing",
    "Enhanced mocking framework",
    "Updated test documentation",
    "Improved assertion patterns",
    "Added regression tests",
    "Enhanced test configuration",
    # Documentation
    "Updated API documentation",
    "Enhanced code comments",
    "Added usage examples",
    "Improved README structure",
    "Updated changelog entries",
    "Enhanced docstring coverage",
    "Added configuration guide",
    "Improved troubleshooting docs",
    "Updated migration guide",
    "Enhanced developer guide",
    # Dependencies & Build
    "Updated project dependencies",
    "Enhanced build configuration",
    "Optimized dependency tree",
    "Updated package metadata",
    "Improved CI/CD pipeline",
    "Enhanced deployment scripts",
    "Updated environment configuration",
    "Optimized build artifacts",
    "Enhanced release workflow",
    "Updated container configuration",
    # Security
    "Enhanced security measures",
    "Updated encryption protocols",
    "Improved access controls",
    "Enhanced input validation",
    "Updated authentication tokens",
    "Improved session management",
    "Enhanced data sanitization",
    "Updated security headers",
    "Improved vulnerability patches",
    "Enhanced audit logging",
    # Performance
    "Optimized query performance",
    "Enhanced memory management",
    "Improved load times",
    "Reduced latency bottlenecks",
    "Optimized database indexes",
    "Enhanced resource utilization",
    "Improved concurrent processing",
    "Optimized network requests",
    "Enhanced data streaming",
    "Improved garbage collection",
    # Architecture
    "Refined architectural patterns",
    "Enhanced module separation",
    "Improved dependency injection",
    "Enhanced service layer abstraction",
    "Updated repository pattern",
    "Improved event-driven architecture",
    "Enhanced middleware pipeline",
    "Updated factory patterns",
    "Improved observer implementation",
    "Enhanced strategy pattern usage",
    # Maintenance
    "Performed routine maintenance",
    "Applied system updates",
    "Cleaned up temporary files",
    "Optimized storage usage",
    "Enhanced backup procedures",
    "Updated recovery protocols",
    "Improved monitoring setup",
    "Enhanced alerting rules",
    "Updated logging levels",
    "Optimized cron schedules",
    # Configuration
    "Updated application settings",
    "Enhanced configuration management",
    "Improved environment variables",
    "Updated default parameters",
    "Enhanced feature flags",
    "Improved runtime configuration",
    "Updated schema definitions",
    "Enhanced migrations system",
    "Improved seeding logic",
    "Updated fixture data",
    # UI/UX
    "Enhanced user interface elements",
    "Improved responsive design",
    "Updated component library",
    "Enhanced accessibility features",
    "Improved color scheme contrast",
    "Updated typography settings",
    "Enhanced form validation UI",
    "Improved navigation structure",
    "Updated animation timing",
    "Enhanced loading states",
    # Database
    "Optimized database queries",
    "Enhanced connection pooling",
    "Updated migration scripts",
    "Improved data normalization",
    "Enhanced indexing strategy",
    "Updated schema relations",
    "Improved transaction handling",
    "Enhanced data integrity checks",
    "Updated stored procedures",
    "Optimized query plans",
    # Networking
    "Enhanced API endpoint responses",
    "Improved request handling",
    "Updated rate limiting rules",
    "Enhanced websocket connections",
    "Improved DNS resolution",
    "Enhanced SSL/TLS configuration",
    "Updated proxy settings",
    "Improved load balancing",
    "Enhanced failover mechanisms",
    "Improved timeout handling",
    # DevOps
    "Enhanced Docker configuration",
    "Improved Kubernetes manifests",
    "Updated Terraform scripts",
    "Enhanced Ansible playbooks",
    "Improved Helm charts",
    "Updated monitoring dashboards",
    "Enhanced logging aggregation",
    "Improved metric collection",
    "Updated alert thresholds",
    "Enhanced auto-scaling rules",
    # Additional Messages
    "Applied hotfix for critical bug",
    "Backported security patches",
    "Deprecated legacy endpoints",
    "Removed unused dependencies",
    "Consolidated duplicate utilities",
    "Standardized error codes",
    "Normalized data formats",
    "Harmonized API responses",
    "Unified logging patterns",
    "Synchronized configuration files",
    "Rectified edge case behavior",
    "Mitigated potential race condition",
    "Addressed memory leak issue",
    "Patched cross-site scripting vulnerability",
    "Fortified authentication mechanism",
    "Strengthened authorization checks",
    "Bolstered input sanitization",
    "Reinforced validation pipeline",
    "Escalated error reporting",
    "Refined fallback strategies",
    "Extended timeout boundaries",
    "Adjusted concurrency limits",
    "Tuned connection parameters",
    "Calibrated performance metrics",
    "Aligned with coding standards",
    "Conformed to style guidelines",
    "Revised naming conventions",
    "Updated formatting rules",
    "Enforced linting rules",
    "Applied code formatting",
    "Restructured directory layout",
    "Reorganized module exports",
    "Redistributed responsibilities",
    "Decoupled tightly bound components",
    "Extracted reusable utilities",
    "Simplified complex logic",
    "Streamlined data flow",
    "Clarified ambiguous conditions",
    "Untangled nested control flow",
    "Consolidated scattered logic",
    "Expanded test scenarios",
    "Diversified test data sets",
    "Strengthened assertion coverage",
    "Fleshed out boundary tests",
    "Added stress testing suite",
    "Benchmarked critical paths",
    "Profiled CPU utilization",
    "Traced memory allocation patterns",
    "Analyzed I/O bottlenecks",
    "Inspected thread contention",
    "Augmented developer tooling",
    "Enhanced debugging capabilities",
    "Added profiling hooks",
    "Instrumented key metrics",
    "Implemented telemetry collection",
    "Enabled verbose logging mode",
    "Configured structured logging",
    "Established log rotation policies",
    "Defined retention strategies",
    "Archived old log data",
    "Catalogued API versions",
    "Tagged release candidates",
    "Published beta builds",
    "Staged rolling updates",
    "Coordinated release schedule",
    "Validated upgrade paths",
    "Tested downgrade procedures",
    "Verified rollback mechanisms",
    "Certified release artifacts",
    "Signed distribution packages",
    "Boosted compilation flags",
    "Minified production assets",
    "Tree-shook unused exports",
    "Code-split large bundles",
    "Lazy-loaded heavy components",
    "Prefetched critical resources",
    "Cached static assets",
    "CDN-distributed media files",
    "Gzipped transfer payloads",
    "Brotli-compressed responses",
    "Planned capacity upgrades",
    "Forecasted resource demands",
    "Provisioned additional nodes",
    "Scaled horizontal clusters",
    "Distributed shard keys",
    "Replicated read instances",
    "Failed-over to standby region",
    "Recovered from backup snapshot",
    "Restored point-in-time data",
    "Validated backup integrity",
    "Reviewed access logs",
    "Audited permission changes",
    "Rotated API credentials",
    "Refreshed TLS certificates",
    "Revoked compromised tokens",
    "Inspected network traffic",
    "Analyzed threat patterns",
    "Blocked malicious requests",
    "Quarantined suspicious activity",
    "Hardened system configuration",
    "Wrote architectural decision record",
    "Drafted RFC for new proposal",
    "Commented on design review",
    "Addressed PR feedback",
    "Resolved merge conflicts",
    "Rebased feature branch",
    "Squashed intermediate commits",
    "Cherry-picked critical fix",
    "Reverted breaking change",
    "Tagged stable release point",
]

# ═════════════════════════════════════════════════════════════════════════ #
#  THEME & STYLES                                                          #
# ═════════════════════════════════════════════════════════════════════════ #

custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "brand": "bold blue",
        "highlight": "bold magenta",
        "dim": "grey50",
        "accent": "bold yellow",
    }
)

console = Console(theme=custom_theme, highlight=False)

# ═════════════════════════════════════════════════════════════════════════ #
#  BRAND & UI COMPONENTS                                                   #
# ═════════════════════════════════════════════════════════════════════════ #

BOX_WIDTH = 140


def spin_animation(message: str, duration: float = 1.5) -> None:
    """Show a spinner animation for the given duration."""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r\x1b[36m{chars[i % len(chars)]}\x1b[0m {message}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r\x1b[32m\u2713\x1b[0m {message}  ")


def print_credit_splash() -> None:
    """Show structured branded splash with signature wordmark, no author name."""
    width = min(BOX_WIDTH, console.width - 2)
    date_now = datetime.now().strftime("%Y-%m-%d")

    meta_line = Text.from_markup(
        f"[black on bright_green] {VERSION} [/black on bright_green]  "
        f"[black on green] {date_now} [/black on green]  "
        f"[black on bright_blue] {BUILD} [/black on bright_blue]"
    )

    wordmark = Panel(
        Align.center(Text("  \U0001d4dc   \U0001d4da   \U0001d4e1   -   \U0001d4d8   \U0001d4dd   \U0001d4d5   \U0001d4d8   \U0001d4dd   \U0001d4d8   \U0001d4e3   \U0001d4e8  ", style="bold white")),
        box=box.ROUNDED,
        border_style="bright_green",
        style="on black",
        padding=(1, 6),
    )

    title_line = Panel(
        Align.center(Text("BULK COMMIT GENERATOR", style="bold white")),
        box=box.HEAVY,
        border_style="bright_green",
        style="on black",
        padding=(0, 10),
    )

    social_line = Text.from_markup(
        f"[bold white]{GITHUB_LOGO}[/bold white]  [link={GITHUB_URL}][green]{USERNAME}[/green][/link]  "
        f"[dim]│[/dim]  "
        f"[bold white]{INSTAGRAM_LOGO}[/bold white]  [link={INSTAGRAM_URL}][green]{INSTAGRAM_ID}[/green][/link]  "
        f"[dim]│[/dim]  "
        f"[dim]📦[/dim] [link={REPOSITORY_URL}][bold green]most-commited[/bold green][/link]"
    )

    chips = Table.grid(padding=(0, 1))
    chips.add_column(justify="center")
    chips.add_column(justify="center")
    chips.add_column(justify="center")
    chips.add_row(
        "[black on bright_green] REAL COMMITS [/black on bright_green]",
        "[black on green] SIGNED / UNSIGNED [/black on green]",
        "[black on bright_yellow] FAST BULK MODE [/black on bright_yellow]",
    )

    notice = Panel(
        Align.center(Text.from_markup(
            f"[bold yellow]⚠ NOTICE:[/bold yellow]  "
            f"If you modify, redistribute, fork, or reuse this project, please "
            f"provide proper credit to [bold green]{AUTHOR}[/bold green] ([bold green]{USERNAME}[/bold green])  "
            f"[dim]|[/dim]  [green]{REPOSITORY_URL}[/green]"
        )),
        box=box.ROUNDED,
        border_style="yellow",
        padding=(0, 2),
    )

    content = Table.grid(expand=True)
    content.add_column(justify="center")
    content.add_row(Align.center(meta_line))
    content.add_row("")
    content.add_row(Align.center(wordmark))
    content.add_row("")
    content.add_row(Align.center(title_line))
    content.add_row(Align.center(Text("Professional Git Activity Automation", style="italic green")))
    content.add_row("")
    content.add_row(Align.center(social_line))
    content.add_row("")
    content.add_row(Align.center(chips))
    content.add_row("")
    content.add_row(Align.center(notice))
    content.add_row("")
    content.add_row(Align.center(Text(COPYRIGHT, style="dim italic")))

    splash = Panel(
        Align.center(content),
        box=box.DOUBLE,
        border_style="bright_green",
        padding=(1, 2),
        width=width,
        title="[bold green]\U0001f680 Bulk Commit Generator[/bold green]",
        subtitle=f"[bold green]{USERNAME}[/bold green]",
        title_align="center",
        subtitle_align="center",
    )

    with Live(console=console, refresh_per_second=10, transient=True) as live:
        for idx, step in enumerate([
            "🎨 Painting brand", "🔗 Linking platforms", "🚀 Launching",
        ], start=1):
            loading = Panel(
                Align.center(Text.from_markup(
                    f"\n[bold green]{step}[/bold green]\n"
                    f"[bright_green]{'●' * idx}[/bright_green][dim]{'○' * (3 - idx)}[/dim]\n"
                )),
                box=box.ROUNDED, border_style="green",
                width=min(50, width),
                title="[bold green]Building Launch Box[/bold green]",
                title_align="center",
            )
            live.update(Align.center(loading))
            time.sleep(0.25)

    console.print(Align.center(splash))
    time.sleep(0.8)


def print_banner() -> None:
    """Display the full branded startup banner with animations."""
    console.clear()

    # ── Animated startup sequence ────────────────────────────────────────
    spin_animation("Initializing Bulk Commit Generator...", 1.2)
    spin_animation("Loading assets and modules...", 0.8)
    spin_animation("Preparing user interface...", 0.6)
    time.sleep(0.3)
    console.clear()
    console.print("")

    # ── Single main branded launch box ───────────────────────────────────
    print_credit_splash()

    console.print("")


# ═════════════════════════════════════════════════════════════════════════ #
#  GIT OPERATIONS                                                          #
# ═════════════════════════════════════════════════════════════════════════ #


def run_git_command(
    args: list[str],
    cwd: Optional[str] = None,
    timeout: int = 30,
    env: Optional[dict[str, str]] = None,
) -> Tuple[int, str, str]:
    """Safely execute a Git command using subprocess (never shell=True).

    Args:
        args: List of Git arguments (e.g., ['rev-list', '--count', 'HEAD']).
        cwd: Working directory for the command. Defaults to current.
        timeout: Maximum execution time in seconds.
        env: Additional environment variables (merged with current env).

    Returns:
        Tuple of (returncode, stdout, stderr).
    """
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=cmd_env,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return -1, "", "Git is not installed or not found in PATH."
    except subprocess.TimeoutExpired:
        return -2, "", f"Git command timed out after {timeout} seconds."
    except PermissionError:
        return -3, "", "Permission denied while running Git command."
    except OSError as exc:
        return -4, "", f"OS error: {exc}"


def is_git_repository(path: Optional[str] = None) -> bool:
    """Check if the given path (or current directory) is a Git repository."""
    code, _, _ = run_git_command(["rev-parse", "--git-dir"], cwd=path)
    return code == 0


def get_git_repo_root(path: Optional[str] = None) -> Optional[str]:
    """Get the absolute path of the Git repository root."""
    code, out, _ = run_git_command(["rev-parse", "--show-toplevel"], cwd=path)
    return out if code == 0 else None


def get_current_branch(path: Optional[str] = None) -> Optional[str]:
    """Get the current active branch name."""
    code, out, _ = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
    return out if code == 0 else None


def get_commit_count(path: Optional[str] = None) -> int:
    """Count total commits in the current branch (or return 0 if none)."""
    code, out, _ = run_git_command(["rev-list", "--count", "HEAD"], cwd=path)
    return int(out) if code == 0 else 0


def get_worktree_status(path: Optional[str] = None) -> Tuple[bool, str]:
    """Return whether the repository has uncommitted changes and raw status."""
    code, out, err = run_git_command(["status", "--porcelain"], cwd=path, timeout=20)
    if code != 0:
        return True, err or "Could not read working tree status."
    return bool(out.strip()), out


def get_git_user_name(path: Optional[str] = None) -> Optional[str]:
    """Get the configured Git user name."""
    code, out, _ = run_git_command(["config", "user.name"], cwd=path)
    return out if code == 0 else None


def get_git_user_email(path: Optional[str] = None) -> Optional[str]:
    """Get the configured Git user email."""
    code, out, _ = run_git_command(["config", "user.email"], cwd=path)
    return out if code == 0 else None


def check_signing_config(path: Optional[str] = None) -> Tuple[bool, str, str]:
    """Check if Git signing is properly configured.

    Returns:
        Tuple of (is_configured, signing_key, detail_message).
    """
    # Check commit.gpgSign
    code_sign, out_sign, _ = run_git_command(
        ["config", "--get", "commit.gpgSign"], cwd=path
    )
    # Check user.signingkey
    code_key, out_key, _ = run_git_command(
        ["config", "--get", "user.signingkey"], cwd=path
    )

    if code_sign != 0 or out_sign.lower() not in ("true", "t", "yes", "y", "1"):
        return False, "", "commit.gpgSign is not enabled.\nRun: git config --global commit.gpgSign true"

    if code_key != 0 or not out_key.strip():
        return False, "", (
            "No GPG/SSH signing key found.\n"
            "Generate a key: gpg --full-generate-key\n"
            "List keys:       gpg --list-secret-keys --keyid-format=long\n"
            "Configure:       git config --global user.signingkey <KEY_ID>\n"
            "Add to GitHub:   https://github.com/settings/gpg/new"
        )

    return True, out_key.strip(), "Signing is properly configured."


def stage_file(file_path: str, cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Stage a file for commit using git add."""
    code, _, err = run_git_command(["add", "--", file_path], cwd=cwd, timeout=20)
    if code != 0:
        return False, f"Failed to stage file: {err}"
    return True, ""


def create_unsigned_commit(message: str, cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Create an unsigned Git commit."""
    code, _, err = run_git_command(
        ["commit", "--quiet", "--no-gpg-sign", "-m", message],
        cwd=cwd,
        timeout=60,
        env={"GIT_TERMINAL_PROMPT": "0"},
    )
    if code != 0:
        detail = err or "Git commit failed without returning details."
        return False, f"Failed to create unsigned commit: {detail}"
    return True, ""


def create_signed_commit(message: str, cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Create a signed Git commit (-S flag) with GPG agent support.

    Uses GIT_TERMINAL_PROMPT=0 to prevent hanging on GPG passphrase
    prompts — the GPG agent must already be running and have the key
    cached. Run 'gpg-agent --daemon' or 'export GPG_TTY=$(tty)' first.
    """
    code, _, err = run_git_command(
        ["commit", "--quiet", "-S", "-m", message],
        cwd=cwd,
        timeout=90,
        env={"GIT_TERMINAL_PROMPT": "0"},
    )
    if code != 0:
        detail = err or "Git signing failed without returning details."
        hint = (
            "\n\n[bold yellow]Signing Troubleshooting Tips:[/bold yellow]\n"
            "  1. Cache your signing passphrase before running a huge batch.\n"
            "  2. Run: [bold]export GPG_TTY=$(tty)[/bold]\n"
            "  3. Run: [bold]gpg --list-secret-keys --keyid-format=long[/bold]\n"
            "  4. Test once manually: [bold]git commit -S --allow-empty -m test[/bold]\n"
            "  5. If you do not need signed commits, rerun and choose unsigned mode."
        )
        return False, f"Failed to create signed commit: {detail}{hint}"
    return True, ""


def push_commits(branch: str, cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Push commits to the remote origin."""
    console.print("[info]Pushing commits to remote origin...[/info]")
    try:
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Push timed out after 120 seconds."
    except Exception as exc:
        return False, f"Push failed: {exc}"


# ═════════════════════════════════════════════════════════════════════════ #
#  FILE OPERATIONS                                                         #
# ═════════════════════════════════════════════════════════════════════════ #


def ensure_folder_and_file(folder: str, repo_root: str) -> Tuple[bool, str]:
    """Ensure the target folder and activity.log exist.

    Args:
        folder: Relative folder path (e.g., 'src').
        repo_root: Absolute path to the repository root.

    Returns:
        Tuple of (success, full_path_to_activity_file).
    """
    full_folder = os.path.join(repo_root, folder)
    activity_path = os.path.join(full_folder, ACTIVITY_FILE)

    try:
        os.makedirs(full_folder, exist_ok=True)
        if not os.path.exists(activity_path):
            with open(activity_path, "w", encoding="utf-8") as f:
                f.write("# Activity Log\n")
                f.write(f"# Generated by Bulk Commit Generator {VERSION}\n")
                f.write("# Repository: https://github.com/mkr-infinity/most-commited\n")
                f.write("# Author: Mohammad Kaif Raja (mkr-infinity)\n")
                f.write(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("#" * 70 + "\n")
        return True, activity_path
    except PermissionError:
        return False, f"Permission denied creating folder: {full_folder}"
    except OSError as exc:
        return False, f"OS error creating folder: {exc}"


def append_activity_line(
    activity_path: str,
    commit_number: int,
    emoji: str,
    message: str,
) -> Tuple[bool, str]:
    """Append a new activity line to the activity.log file.

    Args:
        activity_path: Full path to the activity.log file.
        commit_number: Sequential commit number.
        emoji: Random emoji for this commit.
        message: Random activity message for this commit.

    Returns:
        Tuple of (success, line_written).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"Commit #{commit_number} | {timestamp} | {emoji} | {message}\n"
    try:
        with open(activity_path, "a", encoding="utf-8") as f:
            f.write(line)
        return True, line.strip()
    except PermissionError:
        return False, "Permission denied writing to activity file."
    except OSError as exc:
        return False, f"OS error writing to file: {exc}"


# ═════════════════════════════════════════════════════════════════════════ #
#  COMMIT GENERATION ENGINE                                                #
# ═════════════════════════════════════════════════════════════════════════ #


def generate_commits(
    count: int,
    start_number: int,
    folder: str,
    signed: bool,
    repo_root: str,
) -> Tuple[bool, int, float]:
    """Generate the requested number of commits with real file changes.

    Args:
        count: Number of commits to generate.
        start_number: Starting commit number (current count + 1).
        folder: Target folder relative to repo root.
        signed: Whether to use signed commits.
        repo_root: Absolute path to repository root.

    Returns:
        Tuple of (success, commits_generated, elapsed_seconds).
    """
    # Ensure folder and file exist
    success, activity_path = ensure_folder_and_file(folder, repo_root)
    if not success:
        console.print(f"[error]\u274c {activity_path}[/error]")
        return False, 0, 0.0

    activity_path = os.path.join(repo_root, folder, ACTIVITY_FILE)

    # Determine commit function
    commit_fn = create_signed_commit if signed else create_unsigned_commit
    mode_str = "Signed" if signed else "Unsigned"

    start_time = time.time()
    generated = 0

    bar_width = max(20, min(40, console.width - 50)) if console.width else 40
    refresh_every = 1 if count <= 1000 else max(10, count // 1000)

    progress_columns = [
        SpinnerColumn(spinner_name="dots", style="cyan"),
        TextColumn("[progress.description]{task.description:>12}"),
        BarColumn(bar_width=bar_width, complete_style="cyan", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TextColumn("<"),
        TimeRemainingColumn(),
    ]

    with Progress(
        *progress_columns,
        console=console,
        transient=False,
        expand=False,
        auto_refresh=False,
    ) as progress:

        task = progress.add_task(
            f"[bold cyan]Generating {count} commits ({mode_str})[/bold cyan]",
            total=count,
        )

        for i in range(count):
            commit_number = start_number + i
            emoji = random.choice(EMOJI_POOL)
            message_text = random.choice(MESSAGE_POOL)
            commit_message = f"{emoji} Activity Commit #{commit_number} - {message_text}"

            # Update activity.log
            ok, line = append_activity_line(activity_path, commit_number, emoji, message_text)
            if not ok:
                console.print(f"\n[error]\u274c {line}[/error]")
                return False, generated, time.time() - start_time

            # Stage the file
            rel_path = os.path.join(folder, ACTIVITY_FILE)
            ok_stage, err_stage = stage_file(rel_path, cwd=repo_root)
            if not ok_stage:
                console.print(f"\n[error]\u274c {err_stage}[/error]")
                return False, generated, time.time() - start_time

            # Create commit
            ok_commit, err_commit = commit_fn(commit_message, cwd=repo_root)
            if not ok_commit:
                console.print(f"\n[error]\u274c {err_commit}[/error]")
                return False, generated, time.time() - start_time

            generated += 1

            should_refresh = generated == count or generated % refresh_every == 0

            # Avoid expensive terminal redraws on very large commit batches.
            progress.update(
                task,
                advance=1,
                description=(
                    f"[bold cyan]#{commit_number}[/bold cyan] "
                    f"{emoji} [italic]{message_text[:42]}[/italic]"
                ),
                refresh=should_refresh,
            )
            if should_refresh:
                progress.refresh()

    elapsed = time.time() - start_time
    return True, generated, elapsed


# ═════════════════════════════════════════════════════════════════════════ #
#  DISPLAY / SUMMARY HELPERS                                               #
# ═════════════════════════════════════════════════════════════════════════ #


def display_repository_info(repo_root: str, branch: str, commit_count: int) -> None:
    """Display repository statistics in a beautiful table."""
    table = Table(
        title="[bold cyan]\U0001f4e6 Repository Information[/bold cyan]",
        box=box.HEAVY,
        border_style="cyan",
        padding=(0, 2),
        title_justify="center",
    )
    table.add_column("Property", style="bold white", no_wrap=True)
    table.add_column("Value", style="info")

    table.add_row("Repository Path", f"[info]{repo_root}[/info]")
    table.add_row("Current Branch", f"[accent]{branch}[/accent]")
    table.add_row("Total Commits", f"[bold green]{commit_count:,}[/bold green]")
    table.add_row("Author", f"[cyan]{AUTHOR}[/cyan]")
    table.add_row("Repository", f"[link={REPOSITORY_URL}]{REPOSITORY_URL}[/link]")

    console.print(Align.center(table))
    console.print("")


def display_preflight_checks(repo_root: str, branch: str, commit_count: int) -> None:
    """Show a compact, readable preflight checklist before asking questions."""
    dirty, status = get_worktree_status(repo_root)
    checks = Table(
        title="[bold cyan]Preflight Checks[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        show_header=False,
        padding=(0, 1),
    )
    checks.add_column("Status", justify="center", no_wrap=True)
    checks.add_column("Check", style="bold white", no_wrap=True)
    checks.add_column("Result")
    checks.add_row("[green]✓[/green]", "Git", "available")
    checks.add_row("[green]✓[/green]", "Repository", repo_root)
    checks.add_row("[green]✓[/green]", "Branch", branch)
    checks.add_row("[green]✓[/green]", "Commit Count", f"{commit_count:,}")
    checks.add_row(
        "[yellow]![yellow]" if dirty else "[green]✓[/green]",
        "Working Tree",
        "has existing changes" if dirty else "clean",
    )
    console.print(Align.center(checks))

    if dirty:
        preview = "\n".join(status.splitlines()[:8])
        warning = Panel(
            Text.from_markup(
                "[bold yellow]Existing changes detected.[/bold yellow]\n"
                "This tool only stages its selected activity file, but review your worktree first if needed.\n\n"
                f"[dim]{preview}[/dim]"
            ),
            box=box.ROUNDED,
            border_style="yellow",
            width=min(BOX_WIDTH, max(76, console.width - 4)),
            padding=(1, 2),
        )
        console.print(Align.center(warning))
    console.print("")


def display_summary(
    before: int,
    after: int,
    generated: int,
    folder: str,
    file_path: str,
    signed: bool,
    branch: str,
    elapsed: float,
) -> None:
    """Display a comprehensive final summary table."""
    mode_str = "Signed" if signed else "Unsigned"

    avg_cps = generated / elapsed if elapsed > 0 else 0

    # Format execution time
    hours, remainder = divmod(int(elapsed), 3600)
    mins, secs = divmod(remainder, 60)
    time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"

    summary = Table(
        title="[bold green]\u2705 Generation Complete[/bold green]",
        box=box.HEAVY,
        border_style="green",
        padding=(0, 2),
        title_justify="center",
        show_header=False,
    )
    summary.add_column("Key", style="bold white")
    summary.add_column("Value", style="info")

    summary.add_row("Total Commits Before", f"[bold]{before:,}[/bold]")
    summary.add_row("Total Commits After", f"[bold green]{after:,}[/bold green]")
    summary.add_row("Commits Generated", f"[bold green]{generated:,}[/bold green]")
    summary.add_row("Mode", f"[accent]{mode_str}[/accent]")
    summary.add_row("Target Folder", f"[info]{folder}[/info]")
    summary.add_row("Activity File", f"[info]{file_path}[/info]")
    summary.add_row("Branch", f"[accent]{branch}[/accent]")
    summary.add_row("Execution Time", f"[bold]{time_str}[/bold]")
    summary.add_row("Avg Speed", f"[bold green]{avg_cps:.2f}[/bold green] commits/sec")
    summary.add_row("Repository", f"[link={REPOSITORY_URL}]{REPOSITORY_URL}[/link]")

    console.print("")
    console.print(Align.center(summary))
    console.print("")


def display_push_result(success: bool, branch: str, details: str) -> None:
    """Display push result."""
    if success:
        panel = Panel(
            Text.from_markup(
                f"\n[bold green]\u2705 Push Successful![/bold green]\n\n"
                f"Branch: [accent]{branch}[/accent]\n"
                f"Status: [green]Successfully pushed to origin/{branch}[/green]\n"
            ),
            box=box.HEAVY,
            border_style="green",
            padding=(1, 2),
            title="[bold green]\U0001f4e4 Push Result[/bold green]",
            title_align="center",
        )
        console.print(panel)
    else:
        panel = Panel(
            Text.from_markup(
                f"\n[bold red]\u274c Push Failed[/bold red]\n\n"
                f"Branch: [accent]{branch}[/accent]\n"
                f"Error:  [red]{details}[/red]\n\n"
                f"You can push manually:\n"
                f"  [bold]git push origin {branch}[/bold]\n"
            ),
            box=box.HEAVY,
            border_style="red",
            padding=(1, 2),
            title="[bold red]\U0001f4e4 Push Result[/bold red]",
            title_align="center",
        )
        console.print(panel)


def handle_keyboard_interrupt() -> None:
    """Handle Ctrl+C gracefully."""
    console.print("")
    panel = Panel(
        Text.from_markup(
            "\n[bold yellow]\u26a0 Operation Cancelled[/bold yellow]\n\n"
            "The commit generation was interrupted by the user.\n"
            "No data was lost. You can resume from the next commit number.\n"
        ),
        box=box.HEAVY,
        border_style="yellow",
        padding=(1, 2),
    )
    console.print(panel)


# ═════════════════════════════════════════════════════════════════════════ #
#  MAIN APPLICATION LOGIC                                                  #
# ═════════════════════════════════════════════════════════════════════════ #


def parse_cli_args() -> dict:
    """Parse command-line arguments for non-interactive (CI) mode.

    Supports:
        --count N / -c N   Number of commits to generate
        --signed / -s       Sign commits (default: unsigned)
        --push / -p         Auto-push to remote after generation

    Returns dict with keys: count, signed, push, ci_mode.
    """
    args = {"count": 0, "signed": False, "push": False, "ci_mode": False}
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--count", "-c") and i + 1 < len(argv):
            try:
                args["count"] = int(argv[i + 1])
            except ValueError:
                pass
            i += 2
        elif arg in ("--signed", "-s"):
            args["signed"] = True
            i += 1
        elif arg in ("--push", "-p"):
            args["push"] = True
            i += 1
        elif arg in ("--ci", "--non-interactive"):
            args["ci_mode"] = True
            i += 1
        else:
            i += 1
    if args["count"] > 0:
        args["ci_mode"] = True
    return args


def main() -> None:
    """Main entry point for Bulk Commit Generator."""
    cli = parse_cli_args()

    # ── Display Banner ────────────────────────────────────────────────────
    print_banner()

    # ── Git Availability Check ────────────────────────────────────────────
    code_check, _, _ = run_git_command(["--version"])
    if code_check != 0:
        panel = Panel(
            Text.from_markup(
                "\n[bold red]\u274c Git Not Found[/bold red]\n\n"
                "Git is not installed or not available in your PATH.\n\n"
                "Install Git:\n"
                "  Linux:  [bold]sudo apt install git[/bold]\n"
                "  macOS:  [bold]brew install git[/bold]\n"
                "  Windows: [bold]https://git-scm.com/downloads[/bold]\n"
            ),
            box=box.HEAVY,
            border_style="red",
            padding=(1, 2),
        )
        console.print(panel)
        sys.exit(1)

    # ── Repository Detection ──────────────────────────────────────────────
    repo_root = get_git_repo_root()
    branch = None
    commit_count = 0

    if not repo_root:
        if cli["ci_mode"]:
            console.print("[error]\u274c No Git repository detected in CI mode.[/error]")
            sys.exit(1)

        console.print("")
        panel = Panel(
            Text.from_markup(
                "\n[bold yellow]\u26a0 No Git Repository Detected[/bold yellow]\n\n"
                "Current directory is not inside a Git repository.\n\n"
                "You can either:\n"
                "  [bold white][1][/bold white] Provide a path to an existing Git repository\n"
                "  [bold white][2][/bold white] [dim]Exit and run from within a repo[/dim]\n"
            ),
            box=box.HEAVY,
            border_style="yellow",
            padding=(1, 2),
        )
        console.print(panel)
        console.print("")

        try:
            manual_path = Prompt.ask(
                "[bold yellow]Enter path to Git repository[/bold yellow]",
                default="",
            )
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
            sys.exit(0)

        if not manual_path.strip():
            console.print("[info]\U0001f44b Exiting. Please run this tool from within a Git repository.[/info]")
            sys.exit(0)

        manual_path = os.path.abspath(os.path.expanduser(manual_path.strip()))

        if not os.path.isdir(manual_path):
            console.print(f"[error]\u274c Path does not exist: {manual_path}[/error]")
            sys.exit(1)

        if not is_git_repository(manual_path):
            console.print(f"[error]\u274c Not a Git repository: {manual_path}[/error]")
            sys.exit(1)

        repo_root = get_git_repo_root(manual_path)
        if not repo_root:
            console.print("[error]\u274c Could not determine repository root.[/error]")
            sys.exit(1)

        branch = get_current_branch(repo_root)
        commit_count = get_commit_count(repo_root)

        console.print("")
        spin_animation(f"Using repository: {repo_root}", 0.6)

    else:
        branch = get_current_branch()
        commit_count = get_commit_count()

        if not branch:
            console.print("[error]\u274c Could not determine current branch.[/error]")
            sys.exit(1)

    # ── Display Repo Info ─────────────────────────────────────────────────
    display_repository_info(repo_root, branch, commit_count)
    display_preflight_checks(repo_root, branch, commit_count)

    git_name = get_git_user_name(repo_root)
    git_email = get_git_user_email(repo_root)
    if not git_name or not git_email:
        missing = []
        if not git_name:
            missing.append("user.name")
        if not git_email:
            missing.append("user.email")
        panel = Panel(
            Text.from_markup(
                "\n[bold red]\u274c Git Identity Missing[/bold red]\n\n"
                f"Missing Git config: [bold yellow]{', '.join(missing)}[/bold yellow]\n\n"
                "Set your identity in this repository:\n"
                "  [bold]git config user.name \"Your Name\"[/bold]\n"
                "  [bold]git config user.email \"you@example.com\"[/bold]\n\n"
                "Or configure it globally:\n"
                "  [bold]git config --global user.name \"Your Name\"[/bold]\n"
                "  [bold]git config --global user.email \"you@example.com\"[/bold]\n"
            ),
            box=box.HEAVY,
            border_style="red",
            padding=(1, 2),
            width=min(BOX_WIDTH, max(72, console.width - 4)),
        )
        console.print(Align.center(panel))
        sys.exit(1)

    # ── Get Commit Count ─────────────────────────────────────────────────
    rules_panel = Panel(
        Text.from_markup(
            "\n[bold cyan]\U0001f4dd Commit Count Rules[/bold cyan]\n"
            "  \u2022 Must be a positive integer\n"
            "  \u2022 Maximum recommended: 10,000 per session\n"
            "  \u2022 Enter [bold yellow]0[/bold yellow] to exit\n"
        ),
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 1),
    )
    console.print(rules_panel)
    console.print("")

    if cli["ci_mode"] and cli["count"] > 0:
        desired_count = cli["count"]
    else:
        try:
            desired_count = IntPrompt.ask(
                "[bold yellow]How many commits would you like to generate?[/bold yellow]",
                default=10,
            )
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
            sys.exit(0)

    if desired_count <= 0:
        console.print("[info]\U0001f44b Exiting. No commits generated.[/info]")
        sys.exit(0)

    if desired_count > 10000:
        console.print("[warning]\u26a0 Large commit count detected. This may take a while...[/warning]")

    # ── Commit Mode Selection ─────────────────────────────────────────────
    console.print("")
    mode_panel = Panel(
        Text.from_markup(
            "\n[bold cyan]Select Commit Mode[/bold cyan]\n\n"
            "  [bold white][1][/bold white] [green]Signed Commits[/green]  - Requires GPG/SSH signing setup\n"
            "  [bold white][2][/bold white] [info]Unsigned Commits[/info] - Standard Git commits\n"
        ),
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(mode_panel)
    console.print("")

    if cli["ci_mode"]:
        signed = cli["signed"]
    else:
        try:
            mode_choice = Prompt.ask(
                "[bold yellow]Select commit mode[/bold yellow]",
                choices=["1", "2"],
                default="2",
            )
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
            sys.exit(0)

        signed = mode_choice == "1"

    # ── Signing Verification ─────────────────────────────────────────────
    if signed:
        console.print("")
        with console.status("[bold yellow]\U0001f50d Verifying signing configuration...[/bold yellow]"):
            is_configured, key, detail = check_signing_config(repo_root)

        if not is_configured:
            panel = Panel(
                Text.from_markup(
                    f"\n[bold red]\u274c Signing Not Configured[/bold red]\n\n"
                    f"Git signing is not properly configured on this system.\n\n"
                    f"[red]{detail}[/red]\n\n"
                    f"After configuration, you can run this tool again with signed commits.\n"
                ),
                box=box.HEAVY,
                border_style="red",
                padding=(1, 2),
            )
            console.print(Align.center(panel))
            console.print("")
            console.print("[error]Signed mode was selected, so generation has been stopped.[/error]")
            sys.exit(1)
        else:
            panel = Panel(
                Text.from_markup(
                    f"\n[bold green]\u2705 Signing Verified[/bold green]\n\n"
                    f"Signing Key: [accent]{key}[/accent]\n"
                    f"Status:      [green]{detail}[/green]\n"
                ),
                box=box.ROUNDED,
                border_style="green",
                padding=(1, 2),
            )
            console.print(panel)

    # ── Folder Selection ─────────────────────────────────────────────────
    console.print("")
    folder_panel = Panel(
        Text.from_markup(
            "\n[bold cyan]\U0001f4c1 Target Folder[/bold cyan]\n\n"
            "  \u2022 Folder is relative to repository root\n"
            "  \u2022 Will be created automatically if missing\n"
            "  \u2022 Activity file: [info]activity.log[/info] inside this folder\n"
            "  \u2022 Default: [accent]src[/accent]\n\n"
            "Examples:\n"
            "  [dim]src[/dim]\n"
            "  [dim]logs/activity[/dim]\n"
            "  [dim]data/history[/dim]\n"
        ),
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(folder_panel)
    console.print("")

    if cli["ci_mode"]:
        target_folder = DEFAULT_FOLDER
    else:
        try:
            target_folder = Prompt.ask(
                "[bold yellow]Enter target folder[/bold yellow]",
                default=DEFAULT_FOLDER,
            )
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
            sys.exit(0)

        target_folder = target_folder.strip().rstrip("/").lstrip("/")
        if not target_folder:
            target_folder = DEFAULT_FOLDER

    # ── Pre-Generation Summary ────────────────────────────────────────────
    console.print("")
    next_commit = commit_count + 1
    mode_str = "Signed" if signed else "Unsigned"

    pre_table = Table(
        title="[bold cyan]\U0001f680 Pre-Generation Summary[/bold cyan]",
        box=box.HEAVY,
        border_style="cyan",
        padding=(0, 2),
        title_justify="center",
        show_header=False,
    )
    pre_table.add_column("Key", style="bold white")
    pre_table.add_column("Value", style="info")

    pre_table.add_row("Commits to Generate", f"[bold green]{desired_count:,}[/bold green]")
    pre_table.add_row("Starting Number", f"[bold yellow]#{next_commit:,}[/bold yellow]")
    pre_table.add_row("Ending Number", f"[bold green]#{next_commit + desired_count - 1:,}[/bold green]")
    pre_table.add_row("Mode", f"[accent]{mode_str}[/accent]")
    pre_table.add_row("Target Folder", f"[info]{target_folder}[/info]")
    pre_table.add_row("Activity File", f"[info]{target_folder}/{ACTIVITY_FILE}[/info]")
    pre_table.add_row("Repository", f"[info]{repo_root}[/info]")
    pre_table.add_row("Branch", f"[accent]{branch}[/accent]")

    console.print(Align.center(pre_table))
    console.print("")

    # ── Confirmation ──────────────────────────────────────────────────────
    if cli["ci_mode"]:
        proceed = True
    else:
        try:
            proceed = Confirm.ask(
                "[bold yellow]\u2753 Proceed with generation?[/bold yellow]",
                default=True,
            )
        except KeyboardInterrupt:
            handle_keyboard_interrupt()
            sys.exit(0)

        if not proceed:
            console.print("[info]\U0001f44b Generation cancelled by user.[/info]")
            sys.exit(0)

    # ── Generate Commits ─────────────────────────────────────────────────
    console.print("")

    try:
        success, generated, elapsed = generate_commits(
            count=desired_count,
            start_number=next_commit,
            folder=target_folder,
            signed=signed,
            repo_root=repo_root,
        )
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
        console.print(
            "[info]The repository is in a clean state. "
            "You can resume later; the next commit number will continue from the current count.[/info]"
        )
        sys.exit(0)

    console.print("")

    if not success:
        panel = Panel(
            Text.from_markup(
                "\n[bold red]\u274c Generation Failed[/bold red]\n\n"
                "An error occurred during commit generation.\n"
                "Please check the error messages above.\n"
            ),
            box=box.HEAVY,
            border_style="red",
            padding=(1, 2),
        )
        console.print(panel)
        sys.exit(1)

    new_commit_count = get_commit_count(repo_root)

    # ── Update badge.json with new commit count ─────────────────────────
    try:
        badge_path = os.path.join(repo_root, "badge.json")
        import json as _json
        _json.dump(
            {
                "schemaVersion": 1,
                "label": "commits",
                "message": str(new_commit_count),
                "color": "blue",
                "style": "for-the-badge",
                "cacheSeconds": 3600,
            },
            open(badge_path, "w", encoding="utf-8"),
            indent=2,
        )
    except Exception:
        pass

    # ── Final Summary ─────────────────────────────────────────────────────
    display_summary(
        before=commit_count,
        after=new_commit_count,
        generated=generated,
        folder=target_folder,
        file_path=f"{target_folder}/{ACTIVITY_FILE}",
        signed=signed,
        branch=branch,
        elapsed=elapsed,
    )

    # ── Push Option ───────────────────────────────────────────────────────
    console.print("")
    push_panel = Panel(
        Text.from_markup(
            "\n[bold cyan]\U0001f4e4 Push to GitHub?[/bold cyan]\n\n"
            "Push all generated commits to the remote repository.\n"
            f"Branch: [accent]{branch}[/accent]\n"
            f"Remote: [info]origin[/info]\n"
        ),
        box=box.ROUNDED,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(push_panel)
    console.print("")

    if cli["ci_mode"]:
        push_choice = cli["push"]
    else:
        try:
            push_choice = Confirm.ask(
                "[bold yellow]\U0001f504 Push commits to GitHub?[/bold yellow]",
                default=False,
            )
        except KeyboardInterrupt:
            push_choice = False

    if push_choice:
        console.print("")
        push_success, push_details = push_commits(branch, cwd=repo_root)
        display_push_result(push_success, branch, push_details)
        console.print("")

    # ── Farewell ──────────────────────────────────────────────────────────
    farewell_lines = Text.from_markup(
        "\n"
        "[bold cyan]\U0001f680 Bulk Commit Generator[/bold cyan]\n\n"
        "[bold white]Author:[/bold white]     [bold cyan]Mohammad Kaif Raja[/bold cyan] [info](mkr-infinity)[/info]\n"
        f"[bold white]{GITHUB_LOGO} GitHub:[/bold white]    [link={GITHUB_URL}][bold yellow]{USERNAME}[/bold yellow][/link]\n"
        f"[bold magenta]{INSTAGRAM_LOGO} Instagram:[/bold magenta] [link={INSTAGRAM_URL}][bold magenta]{INSTAGRAM_ID}[/bold magenta][/link]\n"
        f"[bold white]Repository:[/bold white] [link={REPOSITORY_URL}]{REPOSITORY_URL}[/link]\n"
        "[dim]Copyright \u00a9 2026 Mohammad Kaif Raja. All Rights Reserved.[/dim]\n"
    )
    farewell = Panel(
        Align.center(farewell_lines),
        box=box.HEAVY,
        border_style="cyan",
        padding=(1, 3),
        width=BOX_WIDTH,
    )
    console.print(Align.center(farewell))


# ═════════════════════════════════════════════════════════════════════════ #
#  ENTRY POINT                                                             #
# ═════════════════════════════════════════════════════════════════════════ #

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
        sys.exit(0)
    except Exception as exc:
        console.print(f"\n[error]\u274c Unexpected error: {exc}[/error]")
        sys.exit(1)
