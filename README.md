# alarm
Softolkを使用した目覚まし(自分用)です。  
https://openweathermap.org/  、Googleカレンダーの各apiを用いて  
今日の天気予報と今日の予定をSoftTolkでしゃべってくれます。

### 使用方法  
https://openweathermap.org/  でアカウントを作成し、APIキーを取得してください。  
<img src="https://user-images.githubusercontent.com/28708899/113668943-f5315a80-96ed-11eb-8ef2-e8ab685f9ad4.jpg" width="380px">  

取得したAPIキーを図に相当する部分に入れ、地名を取得したい地名にすることで情報を取得できます。  
<img src="https://user-images.githubusercontent.com/28708899/113668946-f6fb1e00-96ed-11eb-8d14-341c4ce8ebdc.jpg" width="380px">


また、Googleカレンダーapiで取得したJSONファイルを用いることで予定を取得できます。  
BGMに曲を流したい場合、図の箇所にパスを指定してください。かけない場合は""に設定します。  
<img src="https://user-images.githubusercontent.com/28708899/113669703-16467b00-96ef-11eb-9cc5-5e8a4b8858b4.jpg" widht="380px">  
<img src="https://user-images.githubusercontent.com/28708899/113670045-91a82c80-96ef-11eb-83e2-a8bee6897b2d.jpg" width="380px">

あとはタスクスケジューラ等で起動をセットすることで目覚ましとして使用できると思います。  
