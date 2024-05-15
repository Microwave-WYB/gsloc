"""Command-line interface for querying the Apple location service."""

import argparse
import json
import logging
import sys
from pathlib import Path

import rich
from rich.logging import RichHandler

from gsloc.core import NoResultsError, WifiInfo, query

logger = logging.getLogger(__name__)


def configure_logging(verbose: bool = False):
    """Configures logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
        handlers=[RichHandler()],
    )


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Query the Apple location service for WiFi network locations."
    )
    parser.add_argument(
        "mac_addresses",
        nargs="*",
        help="MAC addresses to query. If not provided, reads from stdin.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Path to a file containing MAC addresses to query, one per line.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to a file to write the results to in GeoJson format.",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def read_mac_addresses_from_file(file_path: Path) -> list[str]:
    """Reads MAC addresses from a file, one per line."""
    with file_path.open() as f:
        return [line.strip() for line in f]


def write_results_to_file(file_path: Path, results: list[WifiInfo]) -> None:
    """Writes the results to a file in GeoJSON format."""
    features = [result.to_feature() for result in results]

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    with file_path.open("w") as f:
        json.dump(geojson, f, indent=2)


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()
    configure_logging(args.verbose)

    if args.input:
        mac_addresses = read_mac_addresses_from_file(args.input)
    elif args.mac_addresses:
        mac_addresses = args.mac_addresses
    else:
        mac_addresses = [line.strip() for line in sys.stdin]

    results: list[WifiInfo] = []
    for mac in mac_addresses:
        try:
            wifi_list = query([mac])
            if wifi_list:
                results.extend(wifi_list)
        except NoResultsError as e:
            logger.warning(str(e))

    if args.output:
        write_results_to_file(args.output, results)
    else:
        rich.print(results)
