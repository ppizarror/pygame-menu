import subprocess
import sys
import shutil
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ScanResult:
    label: str
    success: bool
    skipped: bool = False
    reason: str = ""


def run_cmd(cmd: list[str], label: str) -> ScanResult:
    """Run a shell command."""
    print(f"\n=== {label} ===")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True
        )
        print(result.stdout[:500])  # preview in terminal
        if result.returncode != 0:
            return ScanResult(label=label, success=False)
        return ScanResult(label=label, success=True)

    except FileNotFoundError:
        print(f"[!] Tool not found for {label}")
        return ScanResult(label=label, success=False, skipped=True, reason="tool not found")
    except subprocess.CalledProcessError as e:
        print(f"[!] {label} exited with code {e.returncode}")
        return ScanResult(label=label, success=False)


def check_tool(tool: str) -> bool:
    return shutil.which(tool) is not None


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    scan_dir = repo_root

    print(f"Scanning repository at {scan_dir}")

    if not scan_dir.exists():
        raise FileNotFoundError(f"{scan_dir} does not exist")

    results: list[ScanResult] = []

    # 1) Bandit — skip low severity, skip test files
    if check_tool("bandit"):
        results.append(run_cmd(
            f"bandit -r {repo_root} -ll --exclude {repo_root / 'test'},{repo_root / 'tests'}",
            "Bandit Security Scan",
        ))
    else:
        print("\n[!] Bandit not installed (pip install bandit)")
        results.append(ScanResult(label="Bandit", success=False, skipped=True, reason="not installed"))

    # 2) Semgrep — security rules only
    if check_tool("semgrep"):
        results.append(run_cmd(
            f"semgrep --config p/ci --json --output semgrep_report.json {repo_root}",
            "Semgrep Security Scan",
        ))
    else:
        print("\n[!] Semgrep not installed (pip install semgrep)")
        results.append(ScanResult(label="Semgrep", success=False, skipped=True, reason="not installed"))

    # Summary
    print("\n" + "=" * 50)
    print("SCAN SUMMARY")
    print("=" * 50)
    for r in results:
        if r.skipped:
            status = f"SKIPPED ({r.reason})"
        elif r.success:
            status = "PASSED"
        else:
            status = "FAILED"
        print(f"  {r.label:<35} {status}")

    failed = [r for r in results if not r.success and not r.skipped]
    if failed:
        print(f"\n{len(failed)} scan(s) failed.")
        sys.exit(1)
    else:
        print("\nAll scans passed or skipped.")


if __name__ == "__main__":
    main()