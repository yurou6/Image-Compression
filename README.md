# Image-Compression

設計一個基於Run-Length的壓縮方法，對圖檔作無失真壓縮後儲存成新檔案，並計算三張圖的平均壓縮率(compression ratio)。
> https://yzucs362.blogspot.com/2022/06/s1083340-6.html

實作

Encoding:
1. 使用cv2.imread()讀取圖片
2. 使用cv2.split()將圖像分成b,g,r通道
3. 使用flatten()將各個通道轉成一維
4. 接著針對每一個通道進行RLE編碼,並將原圖片的長、寬、壓所後資料存入npz檔案中
  -其中把b,g,r的資料串接起來
5. 利用原始圖檔大小與壓縮後圖檔資料，計算圖片的壓縮率及平均壓縮率

Decoding:
1. 讀取壓縮檔(.npz)
2. 將b,g,r壓縮資料分別存放
3. 接著針對每一個通道進行RLE解碼
4. 使用np.array()將資料型態轉成array
5. 使用reshape()將各通道資料轉成三維
6. 使用cv2.merge()將b,g,r合併，得到原圖(無失真)

結果

| 圖片 | 原始檔案大小 | 壓縮後檔案大小 | 壓縮率 | 
| --- | --- | --- | --- |
| img1.bmp | 14,332KB | 5,212KB | 2.74802 |
| img2.bmp | 14,332KB | 8,690KB | 1.64813 | 
| img3.bmp | 14,332KB | 4,979KB | 2.87694 |
- 平均壓縮率**2.42436** 
