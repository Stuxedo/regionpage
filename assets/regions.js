/*
 * Stuxedo regions: the one place regions and servers are listed.
 *
 * Adding a region or a server is a single edit here. index.html renders from it, and
 * scripts/build-readme.py copies it into the README's region table.
 *
 * Keep the object below strict JSON (double quotes, no trailing commas, no comments): the
 * script reads it with a JSON parser.
 *
 * brand.domain      the brand's region domain; a region lives at https://<code>.<domain>/
 * region.flag       a flag-icons code (https://flagicons.lipis.dev), or null for no flag
 * region.icon       used when flag is null: the icon drawn in the flag's place
 * server.name       the server's name; its hostname is <name>.servers.<code>.<domain>
 * server.monitor    the slug on the Stux.Group status page, or null when it isn't monitored
 *
 * Regions are listed in the order they appear on the page.
 */
window.REGION_DATA = {
  "brand": {
    "name": "Stuxedo",
    "domain": "stuxedo.net",
    "statusUrl": "https://status.stux.group",
    "statusSummary": "https://raw.githubusercontent.com/StuxGroup/Status/main/data/summary.json"
  },
  "regions": [
    {
      "code": "uk",
      "name": "United Kingdom",
      "flag": "gb",
      "servers": [
        { "name": "robo1", "monitor": "robo1" },
        { "name": "tiny1", "monitor": "tiny1" },
        { "name": "web1", "monitor": null }
      ]
    },
    { "code": "eu", "name": "Europe", "flag": "eu", "servers": [] },
    {
      "code": "es",
      "name": "Spain",
      "flag": "es",
      "servers": [
        { "name": "mixr1", "monitor": "mixr1" }
      ]
    },
    {
      "code": "us",
      "name": "United States",
      "flag": "us",
      "servers": [
        { "name": "down1", "monitor": "down1" }
      ]
    },
    {
      "code": "ca",
      "name": "Canada",
      "flag": "ca",
      "servers": [
        { "name": "kitt1", "monitor": "kitt1" }
      ]
    },
    { "code": "au", "name": "Australia", "flag": "au", "servers": [] },
    { "code": "jp", "name": "Japan", "flag": "jp", "servers": [] },
    { "code": "sg", "name": "Singapore", "flag": "sg", "servers": [] },
    { "code": "in", "name": "India", "flag": "in", "servers": [] },
    { "code": "eco", "name": "Eco", "flag": null, "icon": "leaf", "servers": [] }
  ]
};
