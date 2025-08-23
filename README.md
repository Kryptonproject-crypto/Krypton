# Krypton (KYP)

Krypton is a new open-source cryptocurrency based on **Litecoin**.  
Launched on **July 24, 2025**, Krypton’s goal is to be **fast, lightweight, and accessible to everyone**.  
No premine, no VC funding — just a **clean, community-driven blockchain**.

- 🌐 **Official website:** [krypton-project.com](https://krypton-project.com)  
- 🔎 **Block Explorer:** [explorer](https://krypton-project.com/explorer/index.php)

---

## ⚙️ Technical Specifications

| Parameter              | Value                                      |
|------------------------|--------------------------------------------|
| **Name**               | Krypton                                   |
| **Ticker**             | KYP                                       |
| **Algorithm**          | Scrypt (Proof-of-Work)                    |
| **Block Time**         | 60 seconds                                |
| **Initial Block Reward** | 14.26940639 KYP                          |
| **Reward Halving**     | 50% every 525,600 blocks (~1 year)        |
| **Max Supply**         | 15,000,000 KYP                            |
| **Distribution Duration** | ~31 years                               |
| **Address Prefix**     | `KY...`                                   |
| **Premine**            | None                                      |
| **P2P Port**           | 8369                                      |
| **RPC Port**           | 8370                                      |

---

## 🛠️ Build Instructions

### Requirements (Ubuntu 22.04 / Debian)

```
sudo apt update && sudo apt install -y \
    build-essential libtool autotools-dev automake pkg-config \
    libssl-dev libevent-dev bsdmainutils libboost-all-dev \
    libminiupnpc-dev libzmq3-dev libprotobuf-dev protobuf-compiler \
    qttools5-dev qttools5-dev-tools libqrencode-dev git curl
```

### Install Berkeley DB 4.8

Krypton uses **Berkeley DB 4.8** for wallet compatibility:

```
wget http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
tar -xzvf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=/usr/local
make -j$(nproc)
sudo make install
```

Set environment variables:

```
export BDB_PREFIX="/usr/local"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
```

### Compile Krypton

```
git clone https://github.com/Kryptonproject-crypto/Krypton.git
cd Krypton
./autogen.sh
./configure LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
make -j$(nproc)
```

---

## 🚀 Running Krypton

Start the daemon:

```
./src/kryptond -daemon
```

Check synchronization:

```
./src/krypton-cli getblockchaininfo
```

---

## 🌍 Community

Krypton is open to everyone. You are welcome to:

- 💡 Propose ideas  
- 👩‍💻 Contribute to the code  
- 💳 Launch new wallets  
- 🖧 Run nodes  

Join us on [GitHub](https://github.com/Kryptonproject-crypto/Krypton) or [Discord](https://discord.gg/g8c64BccQZ) and help grow Krypton!  

---

## 📜 License

Krypton is an **open-source project** published under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 Acknowledgements

Thanks to all who support Krypton and believe in a **simple, clean, and community-first blockchain**.
