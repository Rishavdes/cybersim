"""
CyberSim Docker Manager
Handles spinning up and tearing down target environments.
"""
import subprocess
import os
import time


def get_arena_path(level_dir: str) -> str:
    """Get the path to the docker-compose file for a level."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "targets", level_dir)


def start_arena(level_dir: str, target_flag: str = None) -> bool:
    """Start the Docker environment for a level."""
    arena_path = get_arena_path(level_dir)
    compose_file = os.path.join(arena_path, "docker-compose.yml")

    if not os.path.exists(compose_file):
        print(f"[!] No docker-compose.yml found at: {compose_file}")
        return False

    env = os.environ.copy()
    if target_flag:
        env["CYBERSIM_FLAG"] = target_flag

    print(f"\n[🐳 ARENA] Spinning up target environment...")
    result = subprocess.run(
        ["docker-compose", "up", "-d", "--build"],
        cwd=arena_path,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[!] Failed to start arena:\n{result.stderr}")
        return False

    print("[🐳 ARENA] Target is LIVE. Waiting for services...")
    time.sleep(3)
    return True


def stop_arena(level_dir: str):
    """Stop and clean up the Docker environment."""
    arena_path = get_arena_path(level_dir)
    print(f"\n[🐳 ARENA] Shutting down target environment...")
    subprocess.run(
        ["docker-compose", "down", "--remove-orphans"],
        cwd=arena_path,
        capture_output=True,
    )
    print("[🐳 ARENA] Target destroyed.")


def get_container_ip(container_name: str) -> str:
    """Get the IP address of a running container."""
    result = subprocess.run(
        ["docker", "inspect", "-f",
         "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
         container_name],
        capture_output=True, text=True,
    )
    ip = result.stdout.strip()
    return ip if ip else "172.20.0.2"


def check_docker() -> bool:
    """Check if Docker is running."""
    result = subprocess.run(["docker", "info"], capture_output=True)
    return result.returncode == 0
