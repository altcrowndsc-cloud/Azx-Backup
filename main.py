# coding: utf-8
import os
import sys
import time
import asyncio
import discord

os.system("cls" if os.name == "nt" else "clear")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header(status="En attente", compte="Non connecté"):
    clear()
    
    # Dégradé de couleurs pour l'ASCII art
    colors = [
        "[38;2;255;140;0m",   # orange vif
        "[38;2;255;200;0m",   # jaune orangé
        "[38;2;200;255;50m",  # vert-jaune
        "[38;2;50;255;180m",  # cyan-vert
        "[38;2;0;220;255m",   # bleu cyan
        "[38;2;180;120;255m", # violet
    ]
    
    art = [
        "   ___   ________   __  _____ _____  _____ _      _____ ",
        "  / _ \ |___  /\ \ / / |_   _|  _  ||  _  | |    /  ___|",
        " / /_\ \   / /  \ V /    | | | | | || | | | |    \ `--.╝",
        " |  _  |  / /   /   \    | | | | | || | | | |     `--. \ ",
        " | | | |./ /___/ /^\ \   | | \ \_/ /\ \_/ / |____/\__/ /",
        " \_| |_/\_____/\/   \/   \_/  \___/  \___/\_____/\____/  ",
    ]
    
    print("\n")
    for i, ligne in enumerate(art):
        col = colors[i % len(colors)]
        print(col + ligne + "[0m")
    
    # Ligne AZX BACKUP en multicolore
    azx_text = "A Z X   B A C K U P"
    azx_colored = ""
    for i, char in enumerate(azx_text):
        col = colors[i % len(colors)]
        azx_colored += col + char
    azx_colored += "[0m"
    
    print("\n" + "[90m" + "═"*20 + "[0m " + azx_colored + " [90m" + "═"*20 + "[0m\n")
    
    print("[38;2;255;100;100m     SelfBot - Clone & Backup Serveur Discord (2026)[0m")
    print("[38;2;200;200;255m     Risque ban permanent[0m\n")
    
    print("[38;2;180;255;180mCompte     :[0m " + compte)
    print("[38;2;180;255;180mStatut     :[0m " + status)
    print("\n[38;2;255;165;0m" + "═"*70 + "[0m\n")


# ────────────────────────────────────────────────
print_header("Initialisation du self-bot...", "En attente du token")

print("[38;2;255;100;100m" + "═"*70 + "[0m")
print("[38;2;200;255;200mVotre token utilisateur (PAS un token bot !)[0m")
print("[38;2;255;200;100mExemple : MTEyMzQ*****c4OTAxMjM0NTY3***MzIxNDU2N****EyMzQ1Njc4OTA.XYZ[0m")
print("[38;2;255;100;100m" + "═"*70 + "[0m\n")

TOKEN = input("[38;2;180;255;180mToken → [0m").strip()

print_header("En attente des IDs...", "Token saisi")

print("[38;2;255;165;0m" + "═"*70 + "[0m")
print("[38;2;200;200;255mID du serveur SOURCE (celui que vous voulez COPIER)[0m")
print("[38;2;255;165;0mClic droit sur le serveur → Copier ID du serveur[0m")
print("[38;2;255;165;0m" + "═"*70 + "[0m\n")

SOURCE_ID = input("[38;2;180;255;180mID Source → [0m").strip()

print_header("En attente de l'ID cible...", "Source saisi")

print("[38;2;255;165;0m" + "═"*70 + "[0m")
print("[38;2;200;200;255mID du serveur CIBLE (celui que vous voulez REMPLACER)[0m")
print("[38;2;255;100;100mAttention : TOUS les salons et rôles (sauf @everyone) seront supprimés ![0m")
print("[38;2;255;165;0m" + "═"*70 + "[0m\n")

TARGET_ID = input("[38;2;180;255;180mID Cible → [0m").strip()

print_header("Récapitulatif avant lancement", "Prêt à démarrer")
print(f"[38;2;180;255;180mToken     :[0m {TOKEN[:10]}... (masqué)")
print(f"[38;2;180;255;180mSource    :[0m {SOURCE_ID}")
print(f"[38;2;180;255;180mCible     :[0m {TARGET_ID}\n")

confirm = input("[38;2;255;165;0mLancer l'opération ? (oui/non) [0m").strip().lower()

if confirm not in ("oui", "o", "yes", "y"):
    print_header("Opération annulée", "Annulé par l'utilisateur")
    time.sleep(3)
    sys.exit(0)

# =============================================================================
# Le client discord
# =============================================================================

client = discord.Client()

@client.event
async def on_ready():
    print_header("Connecté !", f"{client.user.name} ({client.user.id})")
    print("[38;2;100;255;100mConnexion réussie ! Début du clonage...[0m\n")

    source = client.get_guild(int(SOURCE_ID))
    target = client.get_guild(int(TARGET_ID))

    if not source:
        print("[38;2;255;80;80mErreur : serveur SOURCE introuvable[0m")
        await asyncio.sleep(5)
        await client.close()
        return

    if not target:
        print("[38;2;255;80;80mErreur : serveur CIBLE introuvable[0m")
        await asyncio.sleep(5)
        await client.close()
        return

    print(f"[38;2;180;255;180mSource → {source.name} ({source.id})[0m")
    print(f"[38;2;255;180;180mCible  → {target.name} ({target.id})[0m\n")

    # ----------------------------------------------------------------------
    # 1. Backup
    # ----------------------------------------------------------------------
    print_header("Étape 1/4 : Création de la sauvegarde", client.user.name)
    backup = {"roles": [], "channels": []}

    for r in source.roles:
        if r.is_default():
            continue
        backup["roles"].append({
            "name": r.name,
            "color": r.color.value,
            "hoist": r.hoist,
            "mentionable": r.mentionable,
            "permissions": dict(r.permissions),
            "position": r.position
        })

    for ch in sorted(source.channels, key=lambda c: c.position):
        d = {
            "name": ch.name,
            "type": ch.type.name,
            "position": ch.position,
            "parent_name": ch.category.name if ch.category else None,
        }
        if hasattr(ch, "topic"):     d["topic"] = ch.topic
        if hasattr(ch, "nsfw"):      d["nsfw"] = ch.nsfw
        if hasattr(ch, "slowmode_delay"): d["slowmode"] = ch.slowmode_delay
        if hasattr(ch, "bitrate"):   d["bitrate"] = ch.bitrate
        if hasattr(ch, "user_limit"):d["user_limit"] = ch.user_limit

        overw = {}
        for tgt, ow in ch.overwrites.items():
            if isinstance(tgt, discord.Role):
                key = tgt.name
                allow = [p for p,v in ow.pair()[0] if v]
                deny  = [p for p,v in ow.pair()[1] if v]
                overw[key] = {"allow":allow, "deny":deny}
        d["overwrites"] = overw
        backup["channels"].append(d)

    print(f"[38;2;100;255;100mSauvegarde OK : {len(backup['roles'])} rôles - {len(backup['channels'])} salons[0m\n")
    await asyncio.sleep(1.5)

    # ----------------------------------------------------------------------
    # 2. Nuke cible
    # ----------------------------------------------------------------------
    print_header("Étape 2/4 : Suppression complète de la cible", client.user.name)
    print("[38;2;255;80;80mNUKE EN COURS... NE FERMEZ PAS LA FENÊTRE[0m\n")

    for role in [r for r in target.roles if not r.is_default()]:
        try:
            await role.delete()
            print(f"  - Rôle supprimé : {role.name}")
            await asyncio.sleep(0.6)
        except:
            pass

    for ch in sorted(target.channels, key=lambda x: 0 if x.type.name == "category" else 1, reverse=True):
        try:
            await ch.delete()
            print(f"  - Salon supprimé : {ch.name}")
            await asyncio.sleep(1.0)
        except:
            pass

    print("[38;2;255;165;0mSuppression terminée[0m\n")
    await asyncio.sleep(1.5)

    # ----------------------------------------------------------------------
    # 3. Recréation rôles
    # ----------------------------------------------------------------------
    print_header("Étape 3/4 : Recréation des rôles", client.user.name)
    role_map = {}

    for r in sorted(backup["roles"], key=lambda x: x["position"]):
        try:
            nr = await target.create_role(
                name=r["name"],
                color=discord.Color(r["color"]),
                hoist=r["hoist"],
                mentionable=r["mentionable"],
                permissions=discord.Permissions(**r["permissions"])
            )
            role_map[r["name"]] = nr
            print(f"  + Rôle créé : {nr.name}")
            await asyncio.sleep(1.0)
        except Exception as e:
            print(f"  ! Erreur rôle {r['name']} → {e}")

    # ----------------------------------------------------------------------
    # 4. Recréation salons
    # ----------------------------------------------------------------------
    print_header("Étape 4/4 : Recréation des salons", client.user.name)

    cat_map = {}
    for ch in backup["channels"]:
        overw = {}
        for rname, perms in ch["overwrites"].items():
            role = role_map.get(rname)
            if role:
                po = discord.PermissionOverwrite()
                for p in perms.get("allow", []): setattr(po, p, True)
                for p in perms.get("deny", []):  setattr(po, p, False)
                overw[role] = po

        parent = cat_map.get(ch.get("parent_name"))

        try:
            if ch["type"] == "category":
                nc = await target.create_category(
                    name=ch["name"], overwrites=overw, position=ch["position"]
                )
                cat_map[ch["name"]] = nc
            elif ch["type"] == "text":
                await target.create_text_channel(
                    name=ch["name"], category=parent, overwrites=overw,
                    topic=ch.get("topic"), nsfw=ch.get("nsfw", False),
                    slowmode_delay=ch.get("slowmode", 0), position=ch["position"]
                )
            elif ch["type"] == "voice":
                await target.create_voice_channel(
                    name=ch["name"], category=parent, overwrites=overw,
                    bitrate=ch.get("bitrate", 64000),
                    user_limit=ch.get("user_limit", 0), position=ch["position"]
                )
            print(f"  + Salon créé : {ch['name']}")
            await asyncio.sleep(1.5)
        except Exception as e:
            print(f"  ! Erreur salon {ch['name']} → {e}")

    print_header("CLONAGE TERMINE", client.user.name)
    print("[38;2;100;255;100mOpération terminée avec succès[0m")
    print("[38;2;255;165;0mAttention : Discord peut détecter et bannir ce compte rapidement[0m")
    await asyncio.sleep(12)
    await client.close()


try:
    client.run(TOKEN)
except Exception as e:
    print_header("ERREUR CRITIQUE", "Erreur fatale")
    print(f"[38;2;255;80;80m{e}[0m")
    input("\nAppuyez sur Entrée pour quitter...")