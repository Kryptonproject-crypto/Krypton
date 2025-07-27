# Krypton (KYP)

**Krypton** est une crypto-monnaie open source basée sur Litecoin, pensée pour être rapide, légère, et accessible à tous. Le projet a été lancé le 24 juillet 2025 comme une alternative simple, transparente et sans préminage. Son objectif : offrir une blockchain communautaire, propre, et stable.

---

⚙️ Caractéristiques Techniques

Nom : Krypton

Symbole : KYP

Algorithme : Scrypt 

Temps de bloc : 120 secondes (2 minutes)

Récompense initiale : 30.4414 KYP / bloc

Réduction de récompense : 50 % tous les 262 800 blocs (~1 an)

Durée totale de distribution : ~32 ans

Max supply : 16 000 000 KYP

---

## 📦 Compilation

### Prérequis (Linux)

```bash
sudo apt update && sudo apt install -y \
  build-essential libtool autotools-dev automake pkg-config \
  libssl-dev libevent-dev bsdmainutils libboost-all-dev \
  libminiupnpc-dev libzmq3-dev libprotobuf-dev protobuf-compiler \
  qttools5-dev qttools5-dev-tools libqrencode-dev git curl

Berkeley DB 4.8

Krypton utilise Berkeley DB 4.8 pour la compatibilité avec le wallet.

# Cloner et compiler BDB 4.8
wget http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
tar -xzvf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=/usr/local
make -j$(nproc)
sudo make install

Ajouter BDB à votre environnement :

export BDB_PREFIX="/usr/local"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"


---

🔧 Compilation de Krypton

git clone https://github.com/Kryptonproject-crypto/Krypton.git
cd Krypton
./autogen.sh
./configure LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
make -j$(nproc)


---

🚀 Lancement

Démarrer le daemon :

./src/kryptond -daemon

Vérifier la synchronisation :

./src/krypton-cli getblockchaininfo


---

🌐 Réseau

Port P2P : 9333

Port RPC : 8370

Préfixe d’adresse : KY... (à personnaliser)



---

🙌 Rejoindre la Communauté

Krypton est un projet ouvert à tous. Vous êtes les bienvenus pour :

proposer des idées 💡

contribuer au code 👨‍💻

créer un wallet 📱

lancer des nodes 🌍


Contact / Discord / 


---

💬 Licence

Projet open-source publié sous la licence MIT.


---

❤️ Merci

Merci à toutes les personnes qui soutiennent Krypton et qui croient en une blockchain simple, propre, et communautaire.

---

Pour toute information complémentaire rendez-vous sur notre discord : https://discord.gg/raEe6Ddf