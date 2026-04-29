import os
from pathlib import Path

try:
    from selenium.webdriver import ChromeOptions
except ImportError:
    import sys
    packages_path = Path.cwd() / "env" / "Lib" / "site-packages"
    sys.path.insert(0, f"{packages_path}")
    from selenium.webdriver import ChromeOptions

from config_reader import config
from logger import logger


def get_proxies() -> list[str]:
    """Get proxies from file safely"""
    filepath = Path(config.paths.proxy_file)

    if not filepath.exists():
        logger.warning(f"Proxy file not found at {filepath}")
        return []

    try:
        with open(filepath, encoding="utf-8") as proxyfile:
            proxies = [
                proxy.strip().replace("'", "").replace('"', "")
                for proxy in proxyfile.read().splitlines()
                if proxy.strip()
            ]
        return proxies
    except Exception as e:
        logger.error(f"Error reading proxy file: {e}")
        return []


def install_plugin(
    chrome_options: ChromeOptions,
    proxy_host: str,
    proxy_port: int,
    username: str,
    password: str,
    plugin_folder_name: str,
) -> None:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 3,
        "name": "Chrome Proxy Authentication",
        "background": {
            "service_worker": "background.js"
        },
        "permissions": [
            "proxy", "tabs", "unlimitedStorage", "storage", "webRequest", "webRequestAuthProvider"
        ],
        "host_permissions": ["<all_urls>"],
        "minimum_chrome_version": "108"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %s
            },
            bypassList: ["localhost"]
        }
    };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """ % (proxy_host, proxy_port, username, password)

    plugins_folder = Path.cwd() / "proxy_auth_plugin"
    plugins_folder.mkdir(exist_ok=True)
    plugin_folder = plugins_folder / plugin_folder_name
    plugin_folder.mkdir(exist_ok=True)

    with open(plugin_folder / "manifest.json", "w", encoding="utf-8") as f:
        f.write(manifest_json)
    with open(plugin_folder / "background.js", "w", encoding="utf-8") as f:
        f.write(background_js)

    extension_path = str(plugin_folder.resolve())
    chrome_options.add_argument(f"--load-extension={extension_path}")
