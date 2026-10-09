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
 * region.parent     the code of the region it belongs to (EMEA > Europe > United Kingdom), or none
 *                   for a top-level group; server counts add up through every level
 * region.longName   optional full name, e.g. "Europe, the Middle East and Africa" for EMEA
 * region.flag       a flag-icons code (https://flagicons.lipis.dev), or null for no flag
 * region.icon       used when flag is null: the icon drawn in the flag's place (globe-emea,
 *                   globe-amer and globe-apac face each area; also globe, leaf)
 * server.name       the server's name; its hostname is <name>.servers.<code>.<domain>
 * server.monitor    the slug on the Stuxedo status page, or null when it isn't monitored
 *
 * Regions are listed in the order they appear on the page, each after the region it belongs to.
 */
window.REGION_DATA = {
  "brand": {
    "name": "Stuxedo",
    "domain": "stuxedo.net",
    "statusUrl": "https://status.stuxedo.net",
    "statusSummary": "https://raw.githubusercontent.com/Stuxedo/Status/main/data/summary.json"
  },
  "regions": [
    { "code": "emea", "name": "EMEA", "longName": "Europe, the Middle East and Africa", "flag": null, "icon": "globe-emea", "servers": [] },
    { "code": "eu", "name": "Europe", "parent": "emea", "flag": "eu", "servers": [] },
    {
      "code": "uk",
      "name": "United Kingdom",
      "parent": "eu",
      "flag": "gb",
      "servers": [
        { "name": "robo1", "monitor": "robo1" },
        { "name": "tiny1", "monitor": "tiny1" },
        { "name": "web1", "monitor": null }
      ]
    },
    {
      "code": "es",
      "name": "Spain",
      "parent": "eu",
      "flag": "es",
      "servers": [
        { "name": "mixr1", "monitor": "mixr1" }
      ]
    },
    { "code": "amer", "name": "AMER", "longName": "the Americas", "flag": null, "icon": "globe-amer", "servers": [] },
    {
      "code": "us",
      "name": "United States",
      "parent": "amer",
      "flag": "us",
      "servers": [
        { "name": "down1", "monitor": "down1" }
      ]
    },
    {
      "code": "ca",
      "name": "Canada",
      "parent": "amer",
      "flag": "ca",
      "servers": [
        { "name": "kitt1", "monitor": "kitt1" }
      ]
    },
    { "code": "apac", "name": "APAC", "longName": "Asia-Pacific", "flag": null, "icon": "globe-apac", "servers": [] },
    { "code": "au", "name": "Australia", "parent": "apac", "flag": "au", "servers": [] },
    { "code": "jp", "name": "Japan", "parent": "apac", "flag": "jp", "servers": [] },
    { "code": "sg", "name": "Singapore", "parent": "apac", "flag": "sg", "servers": [] },
    { "code": "in", "name": "India", "parent": "apac", "flag": "in", "servers": [] }
  ]
};
