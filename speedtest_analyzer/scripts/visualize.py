import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os
from pathlib import Path


def parse_speedtest_log(log_file):
    """
    speedtestログファイルを解析してDataFrameに変換する
    """
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(log_file)

        # Timestampをdatetime形式に変換
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Download/Uploadをbps（bits per second）からMbps（Megabits per second）に変換
        df["Download_Mbps"] = df["Download"] / 1_000_000
        df["Upload_Mbps"] = df["Upload"] / 1_000_000

        return df
    except Exception as e:
        print(f"エラー: ログファイルの解析に失敗しました - {e}")
        return None


def visualize_speed_over_time(df, output_dir=None):
    """
    時系列でダウンロード/アップロード速度を可視化する
    """
    if df is None or df.empty:
        print("データがありません。可視化を中止します。")
        return

    # 時系列で可視化
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")

    # ダウンロード速度プロット
    plt.plot(
        df["Timestamp"],
        df["Download_Mbps"],
        marker="o",
        linestyle="-",
        color="#3498db",
        linewidth=2,
        label="Download",
    )

    # アップロード速度プロット
    plt.plot(
        df["Timestamp"],
        df["Upload_Mbps"],
        marker="s",
        linestyle="-",
        color="#e74c3c",
        linewidth=2,
        label="Upload",
    )

    # X軸のフォーマット設定
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
    plt.gcf().autofmt_xdate()  # 日付ラベルを傾ける

    # グラフの設定
    plt.title("Internet Speed Over Time", fontsize=16)
    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Speed (Mbps)", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)

    # Y軸の範囲を少し広げる
    y_min = min(df["Download_Mbps"].min(), df["Upload_Mbps"].min()) * 0.9
    y_max = max(df["Download_Mbps"].max(), df["Upload_Mbps"].max()) * 1.1
    plt.ylim(y_min, y_max)

    # データポイントのラベル（データが10点未満の場合のみ表示）
    if len(df) < 10:
        for i, row in df.iterrows():
            plt.text(
                row["Timestamp"],
                row["Download_Mbps"],
                f"{row['Download_Mbps']:.2f}",
                fontsize=9,
                ha="center",
                va="bottom",
            )
            plt.text(
                row["Timestamp"],
                row["Upload_Mbps"],
                f"{row['Upload_Mbps']:.2f}",
                fontsize=9,
                ha="center",
                va="top",
            )

    plt.tight_layout()

    # 出力ディレクトリが指定されている場合はそこに保存
    if output_dir:
        output_path = Path(output_dir) / "network_speed_over_time.png"
        plt.savefig(output_path, dpi=300)
        print(f"グラフを保存しました: {output_path}")

    plt.show()

    # 統計情報を表示
    print("\n統計情報:")
    print(f"期間: {df['Timestamp'].min()} から {df['Timestamp'].max()}")
    print(f"測定回数: {len(df)}")
    print(f"平均ダウンロード速度: {df['Download_Mbps'].mean():.2f} Mbps")
    print(f"平均アップロード速度: {df['Upload_Mbps'].mean():.2f} Mbps")
    print(f"最大ダウンロード速度: {df['Download_Mbps'].max():.2f} Mbps")
    print(f"最大アップロード速度: {df['Upload_Mbps'].max():.2f} Mbps")
    print(f"最小ダウンロード速度: {df['Download_Mbps'].min():.2f} Mbps")
    print(f"最小アップロード速度: {df['Upload_Mbps'].min():.2f} Mbps")


def main():
    # プロジェクトのルートディレクトリ
    project_root = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    # ログファイルと出力ディレクトリのパス
    log_file = project_root / "internet_speed.log"
    output_dir = project_root / "reports"

    # 出力ディレクトリが存在しない場合は作成
    output_dir.mkdir(exist_ok=True)

    print(f"ログファイル: {log_file}")
    print(f"出力ディレクトリ: {output_dir}")

    # データの解析と可視化
    df = parse_speedtest_log(log_file)
    visualize_speed_over_time(df, output_dir)


if __name__ == "__main__":
    main()
