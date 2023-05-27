This Project to Calculate Fundamental Analysis Stock
Data is from Yahoo Finance (using yahooquery, https://yahooquery.dpguthrie.com/)

Yahoo Finance Parameters
1. Total Pendapatan
[Bukan Kumulatif]
([Income Statement] Total Revenue)

2. Laba (rugi) yang dapat diatribusikan ke entitas induk
[Bukan kumulatif]
([Income Statement] Net Income Common Stockholders)

3. Outstanding shares
([Balance Sheet] Shared Issued)

4. Jumlah eukitas yang diatribusikan kepada pemilik induk
([Balance sheet] Stockholder's Equitty)



Fundamental Data (Quarter Time Frame)
1. NPM
Formula = (Laba rugi)/total pendapatan

2. ROE
Formula = ((Laba rugi kumulatif * 4)/(i))/[Ekuitas]
dengan i = Quarter ke-i

3. EPS
Formula = ((Laba rugi kumulatif * 4)/(i))/[Out_shares]
dengan i = Quarter ke-i

4. PER
Formula = Harga Saham per tanggal Laporan/EPS

5. BV
Formula = Ekuitas/Out_shares

6. PBV
Formula = Harga Saham per tanggal Laporan/BV