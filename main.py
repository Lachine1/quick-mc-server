from requests import get
import os
os.mkdir("server")
os.chdir("server")
def get_latest_build(version):
    print(f"Checking latest build of {version}... ")
    req = get(f"https://api.papermc.io/v2/projects/paper/versions/{version}")
    req.raise_for_status()
    builds = req.json()["builds"]
    del req
    return builds[-1]
def download_build(version, build):
    print(f"Downloading build {build} for {version}...")
    build_url = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/paper-{version}-{build}.jar"
    req = get(build_url, stream=True)
    with open(build_url.split("/")[-1], "wb") as jar:
        for chunk in req.iter_content(chunk_size=10 * 1000):
            jar.write(chunk)
    print(f"Download finished")
    del req
def download_plugins(urls):
    os.mkdir("plugins")
    os.chdir("plugins")
    for url in urls:
        print(f"Downloading {url.split('/')[-1]}")
        req = get(url, stream=True)
        with open(url.split("/")[-1], "wb") as jar:
            for chunk in req.iter_content(chunk_size=10 * 1000):
                jar.write(chunk)


if __name__ == "__main__":
    if not input("Do you agree to Minecraft's EULA? (https://aka.ms/MCUsageGuidelines): ").lower().startswith("y"): exit()
    with open("eula.txt", "w") as eula:
        eula.write("eula=true")
    version = input("Version to install (1.8.8 to 1.20.4): ")
    latest_build = get_latest_build(version)
    download_build(version, latest_build)
    download_plugins(
        ("https://github.com/EssentialsX/Essentials/releases/download/2.20.1/EssentialsX-2.20.1.jar",
        "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaBackwards/versions/4.9.1/PAPER/ViaBackwards-4.9.1.jar",
        "https://hangarcdn.papermc.io/plugins/ViaVersion/ViaVersion/versions/4.9.2/PAPER/ViaVersion-4.9.2.jar",
        "https://hangarcdn.papermc.io/plugins/Flyte/PluginPortal/versions/1.5.0/PAPER/PluginPortal-1.5.0.jar",
        "https://hangarcdn.papermc.io/plugins/pop4959/Chunky/versions/1.3.136/PAPER/Chunky-1.3.136.jar",
        "https://hangarcdn.papermc.io/plugins/jmp/TabTPS/versions/1.3.22/PAPER/tabtps-spigot-1.3.22.jar"))
    print("Setup done!\nTo start the server on Linux: cd server && java -jar -Xmx1G -Xms1G paper* (set 1G to how much RAM you want the server to use)\nTo start the server on Windows: Navigate to server folder and run the Paper file.")
