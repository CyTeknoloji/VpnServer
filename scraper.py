import urllib.request
import re

# İnternetteki güncel ve ücretsiz V2Ray havuzları (Bu listeyi istediğin kadar artırabilirsin)
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub"
]

def fetch_servers():
    all_vmess_links = set() # Aynı linkleri tekrar eklememek için Set kullanıyoruz

    for url in SOURCES:
        try:
            print(f"Taranıyor: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                # Gelen veriyi okuyup metne çeviriyoruz (genelde base64 şifrelidir)
                html = response.read()
                try:
                    # Genelde bu havuzlar tüm listeyi base64 ile şifreler, onu çözüyoruz
                    import base64
                    decoded_text = base64.b64decode(html).decode('utf-8')
                except:
                    # Eğer şifreli değilse düz metin olarak al
                    decoded_text = html.decode('utf-8')

                # İçinden sadece vmess:// ile başlayan satırları ayıklıyoruz
                lines = decoded_text.splitlines()
                for line in lines:
                    if line.startswith("vmess://"):
                        # Emojileri ve gereksiz kuyrukları temizliyoruz (Daha önce konuştuğumuz hata olmasın diye)
                        clean_link = line.split(" ")[0].split("#")[0].strip()
                        all_vmess_links.add(clean_link)
        except Exception as e:
            print(f"Hata oluştu ({url}): {e}")

    # Toplanan linkleri v2ray_nodes.txt dosyasına yazıyoruz
    # Uygulama yorulmasın diye mesela en fazla 50 tane taze sunucu yazdırıyoruz
    with open("v2ray_nodes.txt", "w", encoding="utf-8") as f:
        for link in list(all_vmess_links)[:50]:
            f.write(link + "\n")
            
    print(f"Başarılı! Toplam {min(len(all_vmess_links), 50)} adet taze vmess linki kaydedildi.")

if __name__ == "__main__":
    fetch_servers()
