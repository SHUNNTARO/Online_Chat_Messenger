# 概要 
クライアントサーバモデルに沿った最も一般的なソフトウェアであるWebアプリケーションで使用されるているhttpプロトコルを理解するために本アプリを作成しました。　　

httpプロトコル層でreqest,responseを行う際に使用するTCP/UDPを使用してchat appを作成することでTCP/UDPの内部構造についての理解やプロトコルの基本概念を把握すると同時にネットワーキングの基礎を身につけ、サーバサイドのアプリケーション開発のスキルを向上させること目的に取り組んだ。

# 機能要件
サーバはCLIで起動し、UDPネットワークソケットを使用してメッセージのやり取り行いチャットルームの作成と接続をTCPネットワークソケットで行いました。
# 使用技術
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">

# ソケットドメイン一覧
|     キーワード            | 役割                                      | 
| ---------------------- | ----------------------------------------- | 
| ソケット   | 特定のソケットドメインとタイプに基づいて作成され、それぞれがソケットがどのように通信を行うかを決定します。 |
| AF_UNIX   | 同じシステム上のプロセス間通信（IPC）を提供。 |
| AF_INET   | AF_INET は、インターネットプロトコルバージョン 4（IPv4）を使用して、異なるコンピュータシステム上のプロセス間で通信を提供。 |
| AF_INET6   | AF_INET6 は、インターネットプロトコルバージョン 6（IPv6）を使用して、異なるコンピュータシステム上のプロセス間で通信を提供。 |


# キーワード（ソケット）一覧
|     キーワード            | 役割                                      | 
| ---------------------- | ----------------------------------------- | 
| TCP   | TCP はトランスポート層のプロトコルの一つで、信頼性の高いデータ転送を提供。TCP を使用すると、データはパケットに分割され、ネットワークを通じて送信される。送信側は各パケットにシーケンス番号を付け、受信側はこれらのパケットを正しい順序で再組み立てる。また、パケットが失われた場合やエラーが発生した場合は、再送信を行う。 |
| UDP   | UDP はトランスポート層のプロトコルの一つ。TCP とは異なり、UDP は接続レスで信頼性の低い通信を提供。UDP では、パケットの送信が試みられますが、それらが宛先に到達するかどうかは保証されない。また、パケットの順序も保証されず、パケットの再送信も行われない。 |
| SOCK_STREAM  | 信頼性の高い、順序通りの、エラーのないバイトストリームの伝送を提供。これは通常、トランスポート層の TCP プロトコルを使用される。 |
| SOCK_DGRAM   | SOCK_DGRAM は、データグラム（独立したパケット）の送受信を提供。これは通常、トランスポート層の UDP プロトコルを使用される。ソケットが一度接続されると、データは個々のパケットとして送受信される。 |

# メソッド一覧
|     キーワード            | 役割                                      | 
| ---------------------- | ----------------------------------------- | 
| ソケット   | 特定のソケットドメインとタイプに基づいて作成され、それぞれがソケットがどのように通信を行うかを決定します。 |
| AF_UNIX   | 同じシステム上のプロセス間通信（IPC）を提供。 |
| AF_INET   | AF_INET は、インターネットプロトコルバージョン 4（IPv4）を使用して、異なるコンピュータシステム上のプロセス間で通信を提供。 |
| AF_INET6   | AF_INET6 は、インターネットプロトコルバージョン 6（IPv6）を使用して、異なるコンピュータシステム上のプロセス間で通信を提供。 |
