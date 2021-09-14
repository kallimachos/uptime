#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UptimeRobot CLI."""

import requests
from codetiming import Timer
from colorama import Fore, Style
from decouple import config

status_color = {
    "0": f"{Fore.BLUE}PAUSED{Fore.RESET}",
    "1": f"{Style.DIM}WAITING{Style.RESET_ALL}",
    "2": f"{Fore.GREEN}UP{Fore.RESET}",
    "8": f"{Fore.YELLOW}DOWN?{Fore.RESET}",
    "9": f"{Fore.RED}DOWN{Fore.RESET}",
}


def monitor() -> None:
    """Display monitor."""
    with Timer(text="Seconds:{:>8.2f}\n"):
        url = "https://api.uptimerobot.com/v2/getMonitors"
        data = f"api_key={config('API_KEY')}&format=json&all_time_uptime_ratio=1"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }
        r = requests.post(url, data=data, headers=headers)
        result = r.json()
        print(f"\nStatus{'':<4}Uptime{'':<4}Name{'':<11}URL")
        print("--------|---------|--------------|------------------------------------------------")
        for monitor in result["monitors"]:
            status = status_color[str(monitor["status"])]
            ratio = f"{monitor['all_time_uptime_ratio'].split('.')[0]}%"
            name = monitor["friendly_name"]
            url = monitor["url"]
            print(f"{status:<20}{ratio:<10}{name:<15}{url}")
        print()
    return


if __name__ == "__main__":
    monitor()
