# TFMeasure

伝達関数測定用GUIソフト

TFMeasureを実行する前に以下のURLからdouki_c_programsとspeaker_selecterをセットアップする必要があります。

- https://github.com/kudolab/douki_c_programs
- https://github.com/kudolab/speaker_selecter

TFMeaureには以下のファイルが必要です
- BPFBPFBPF100-13k_48k_0-255.DDB バンドパスフィルタ
- DOUKI_START オーディオ入出力の遅延補正用
- TFMeasure 実行用コマンド
- TFMeasure.py メインコード
- measure.py 伝達関数測定用スクリプト
- cpyconv.py C-pythonコンバータ
- rpi_client.py スピーカーセレクターのHTTPクライアント
- m14.DSB 測定用M系列

以下のファイルは測定時に生成される一時的なファイルですので削除しても問題ありません．
- amdama.DDA
- tmp.DSB
- __pycache__

作成者: 下川原 綾汰 (sr17805@tomakomai.kosen-ac.jp)
作成年: 2019

修正者: 瀧澤 哲 (tt20805@tomakomai.kosen-ac.jp)
修正年: 2021
