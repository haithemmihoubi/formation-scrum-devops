# Module 04 — Linux : Gestion des paquets & Stockage

🎯 **Objectif** : installer des logiciels et gérer disques, partitions et systèmes de fichiers.

## 1. Les gestionnaires de paquets

Chaque famille de distribution a son gestionnaire :

| Famille | Gestionnaire | Format |
|---------|--------------|--------|
| Debian / Ubuntu | `apt`, `dpkg` | `.deb` |
| RHEL / CentOS / Rocky / Fedora | `dnf`, `yum`, `rpm` | `.rpm` |
| Alpine | `apk` | `.apk` |
| Arch | `pacman` | |

## 2. APT (Debian / Ubuntu)

```bash
sudo apt update                  # met à jour la liste des paquets
sudo apt upgrade                 # met à jour les paquets installés
sudo apt install nginx           # installer un paquet
sudo apt install -y git curl     # installer sans confirmation
sudo apt remove nginx            # désinstaller (garde la config)
sudo apt purge nginx             # désinstaller + config
sudo apt autoremove              # supprime les dépendances inutiles
apt search docker                # rechercher un paquet
apt show nginx                   # infos sur un paquet
dpkg -l                          # liste des paquets installés
dpkg -L nginx                    # fichiers installés par un paquet
```

💡 Toujours faire `apt update` **avant** un `apt install`.

## 3. DNF / YUM (RHEL / CentOS / Rocky)

```bash
sudo dnf check-update            # vérifier les mises à jour
sudo dnf update                  # tout mettre à jour
sudo dnf install nginx           # installer
sudo dnf remove nginx            # désinstaller
dnf search docker                # rechercher
dnf info nginx                   # infos
rpm -qa                          # paquets installés
```

## 4. APK (Alpine — très utilisé dans Docker)

```bash
apk update
apk add nginx curl
apk del nginx
apk search git
```

Alpine est très léger → image Docker de base populaire.

## 5. Installer depuis les sources / binaires

```bash
# Télécharger un binaire
curl -LO https://example.com/outil
chmod +x outil
sudo mv outil /usr/local/bin/

# Compilation classique (rare en DevOps mais à connaître)
./configure
make
sudo make install
```

## 6. Comprendre le stockage

```bash
lsblk            # liste les disques et partitions (arborescence)
fdisk -l         # détails des disques (root)
df -h            # espace utilisé par système de fichiers
df -i            # nombre d'inodes
du -sh /var      # taille d'un dossier
blkid            # UUID et types des partitions
```

Exemple de sortie `lsblk` :
```
NAME   SIZE TYPE MOUNTPOINT
sda     50G disk
├─sda1   1G part /boot
└─sda2  49G part /
```

## 7. Partitionner et formater

```bash
sudo fdisk /dev/sdb              # partitionner (interactif)
sudo mkfs.ext4 /dev/sdb1         # formater en ext4
sudo mkfs.xfs /dev/sdb1          # formater en xfs
```

Systèmes de fichiers courants : **ext4** (standard Linux), **xfs** (gros volumes), **btrfs**, **vfat** (compatibilité Windows).

## 8. Monter et démonter

```bash
sudo mkdir /mnt/data
sudo mount /dev/sdb1 /mnt/data   # monter une partition
sudo umount /mnt/data            # démonter
mount                            # voir les montages actifs
```

Montage **permanent** via `/etc/fstab` :
```
# <device>          <point de montage>  <type>  <options>  <dump> <pass>
UUID=xxxx-xxxx       /mnt/data           ext4    defaults   0      2
```
```bash
sudo mount -a    # teste/applique le fstab
```

⚠️ Une erreur dans `/etc/fstab` peut empêcher le serveur de démarrer. Toujours tester avec `mount -a`.

## 9. LVM (Logical Volume Manager) — notion

LVM ajoute une couche d'abstraction pour redimensionner le stockage à chaud.

```
Disques physiques (PV) → Groupe de volumes (VG) → Volumes logiques (LV)
```

```bash
sudo pvcreate /dev/sdb           # créer un volume physique
sudo vgcreate vg_data /dev/sdb   # créer un groupe de volumes
sudo lvcreate -L 10G -n lv_app vg_data  # créer un volume logique
sudo lvextend -L +5G /dev/vg_data/lv_app  # agrandir à chaud
```

## 10. Surveiller l'espace (cas DevOps fréquent)

Un disque plein casse une appli. Réflexes :
```bash
df -h                            # quelle partition est pleine ?
du -sh /var/log/* | sort -h      # quel dossier prend de la place ?
journalctl --vacuum-size=200M    # nettoyer les vieux logs systemd
docker system prune              # nettoyer Docker (images/conteneurs)
```

## Exercices

1. Mettez à jour la liste des paquets et installez `htop` et `tree`.
2. Affichez tous les fichiers installés par le paquet `curl`.
3. Listez les disques et partitions de votre machine.
4. Identifiez la partition la plus remplie sur votre système.
5. Trouvez les 3 plus gros dossiers sous `/var`.
6. Expliquez la différence entre `apt remove` et `apt purge`.

> ✅ Passez au [Module 05 — Bash Scripting](05-bash-scripting.md).
