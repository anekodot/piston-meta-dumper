import requests
import json

print("[*] dumping version manifest from Piston..")

piston_meta_uri = 'https://piston-meta.mojang.com'
print(f"[DBG] piston_meta_uri={piston_meta_uri}")

piston_ver_manifest_req = requests.get(f"{piston_meta_uri}/mc/game/version_manifest_v2.json")

version_manifest = piston_ver_manifest_req.json()
print(f"[!] latest stable: {version_manifest["latest"]["release"]}")
print(f"[!] latest snapshot: {version_manifest["latest"]["snapshot"]}")

print(f"[*] dumping all version manifests..")

version_manifest_uris = []
for version_data in version_manifest["versions"]:
    uri_split = str(version_data["url"]).split("/")
    filename = uri_split[len(uri_split) - 1].replace("%20", " ")

    version_manifest_uris.append(
            { 
                "id": version_data["id"],
                "type": version_data["type"],
                "uri": version_data["url"],
                "file_name": filename
            }
        )

for version_meta in version_manifest_uris:
    print(f"[!] Dumping {version_meta["type"]}: {version_meta["id"]}")

    with open(version_meta["file_name"], "x") as data_file:
        json.dump(requests.get(version_meta["uri"]).json(), data_file)
        print(f"[!] Finished dumping {version_meta["id"]}. Moving on!")