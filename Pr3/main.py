import argparse
import random
from typing import List, Tuple

GRID_SIZE = 30
TOTAL_FLEAS = GRID_SIZE * GRID_SIZE


def build_neighbors(size: int) -> List[List[int]]:
    neighbors: List[List[int]] = []
    for r in range(size):
        for c in range(size):
            idx = r * size + c
            options = []
            if r > 0:
                options.append((r - 1) * size + c)
            if r < size - 1:
                options.append((r + 1) * size + c)
            if c > 0:
                options.append(r * size + (c - 1))
            if c < size - 1:
                options.append(r * size + (c + 1))
            neighbors.append(options)
    return neighbors


def simulate_once(
    steps: int,
    neighbors: List[List[int]],
    rng: random.Random,
) -> Tuple[int, List[int]]:
    positions = list(range(TOTAL_FLEAS))
    for _ in range(steps):
        for i, pos in enumerate(positions):
            positions[i] = rng.choice(neighbors[pos])

    counts = [0] * TOTAL_FLEAS
    for pos in positions:
        counts[pos] += 1

    empty = sum(1 for count in counts if count == 0)
    return empty, counts


def render_grid(counts: List[int], size: int) -> str:
    lines = []
    for r in range(size):
        row = []
        for c in range(size):
            count = counts[r * size + c]
            if count == 0:
                row.append(".")
            elif count == 1:
                row.append("1")
            elif count < 10:
                row.append(str(count))
            else:
                row.append("+")
        lines.append(" ".join(row))
    return "\n".join(lines)


def run_simulation(steps: int, trials: int, seed: int, visualize: bool) -> float:
    rng = random.Random(seed)
    neighbors = build_neighbors(GRID_SIZE)

    if visualize:
        empty, counts = simulate_once(steps, neighbors, rng)
        print("\nVisualization (single trial):")
        print(render_grid(counts, GRID_SIZE))
        print(f"Empty squares in this trial: {empty}\n")

    total_empty = 0
    for _ in range(trials):
        empty, _ = simulate_once(steps, neighbors, rng)
        total_empty += empty

    expected = total_empty / trials
    return expected


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flea random walk simulation on a 30x30 grid.",
    )
    parser.add_argument("--steps", type=int, default=50, help="Number of bell rings")
    parser.add_argument("--trials", type=int, default=200, help="Monte Carlo trials")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Print one sample grid after simulation",
    )
    args = parser.parse_args()

    expected = run_simulation(args.steps, args.trials, args.seed, args.visualize)
    print(
        f"Expected empty squares after {args.steps} rings: {expected:.6f}"
    )


if __name__ == "__main__":
    main()
